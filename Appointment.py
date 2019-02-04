import sys
import pdb
import logging
from time import sleep, time
from datetime import datetime, timedelta

from splinter import Browser

from Parser import Parser, ParseChildIdError, ParseAvailableDatesError
from Utils import poll_on_method


class AppointmentError(Exception):
    pass


class LoginError(AppointmentError):
    pass


class ApptLinkError(AppointmentError):
    pass


class DurationError(AppointmentError):
    pass


class ChildTypeError(AppointmentError):
    pass


class SelectChildrenError(AppointmentError):
    pass


class SelectDateError(AppointmentError):
    pass


class SelectTimeError(AppointmentError):
    pass


class UnableToBookAppointmentError(AppointmentError):
    pass


class FinalizeError(AppointmentError):
    pass


class VerifyError(AppointmentError):
    pass


logging.getLogger('selenium').setLevel(logging.WARNING)


class Appointment:
    """The Appointment is the workhorse of this application.  It will
    attempt to book a child sitting appointment  or appointments at
    the specified time while providing feedback to the AppointmentHandler
    should there be any issues with making the booking."""

    url = 'https://booknow.appointment-plus.com/73kgtt5s/'

    durations = {
        30: '973',
        60: '974',
        90: '975'}

    def __init__(self, store, appointments):
        self.browser = Browser()

        self.store = store
        self.is_store_updated = False
        self.appointments = appointments

        self.parser = Parser()
        self.logger = logging.getLogger('mlh_logger')

    def book(self):
        self.browser.visit(self.url)

        self.login()

        for self.appt in self.appointments:
            self.logger.info("Booking appointment\n{}".format(self.appt))
            try:
                self.select_appointments()
                self.set_duration()
                self.select_child_type()
                self.collect_child_ids()

                self.collect_available_dates()

                if self.appt.datetime.date() not in self.available_dates:
                    raise UnableToBookAppointmentError

                self.select_children()
                self.select_date(self.appt.datetime)

                self.collect_available_times()

                if self.appt.datetime not in self.available_times:
                    raise UnableToBookAppointmentError

                self.select_time()
                self.finalize_appointment()
                self.verify_appointment()

                # Successfully booked appointment
                yield True, self.appt

                sleep(1)  # Wait for a bit before booking the next appointment

            except Exception as ex:
                yield ex, self.appt

        # All appointments have been iterated through
        self.close()

    def update_store(self):
        return self.is_store_updated

    def login(self):
        self.login_fill()
        self.login_click()

    @poll_on_method
    def login_fill(self):
        try:
            self.browser.fill('loginname', self.store.user_data.user)
            self.browser.fill('password', self.store.user_data.password)
        except Exception as ex:
            raise LoginError(ex)

    @poll_on_method
    def login_click(self):
        try:
            self.browser.find_by_value('Log In').click()
        except Exception as ex:
            raise LoginError(ex)

    @poll_on_method
    def close(self):
        self.browser.click_link_by_partial_href('logout')
        sleep(2)
        self.browser.quit()

    @poll_on_method
    def select_appointments(self):
        try:
            self.browser.click_link_by_href(self.url + 'appointments')
        except Exception as ex:
            raise ApptLinkError(ex)

    @poll_on_method
    def set_duration(self):
        try:
            self.browser.find_by_name('service_id').select(self.durations[self.appt.duration])
        except Exception as ex:
            raise DurationError(ex)

    @poll_on_method
    def select_child_type(self):
        child_types = {
            'child': '782',
            'infant': '783'}

        try:
            # Grab the first child name from the appointment list and use that
            # as the key to the user_data.children dictionary to look up the type
            child_type = self.store.user_data.children[self.appt.children[0]].type
            self.browser.find_by_name('e_id').select(child_types[child_type])
        except Exception as ex:
            raise ChildTypeError(ex)

    @poll_on_method
    def collect_child_ids(self):
        self.child_ids = {}
        ids_were_parsed = False
        for name, child in self.store.user_data.children.items():
            if not child.id:
                self.child_ids = self.parser.get_child_ids(self.browser.html)
                ids_were_parsed = True
                break

        if ids_were_parsed:
            self.logger.debug('child_ids : {}'.format(self.child_ids))
            self.logger.debug('persitant child_ids : {}'.format(
                          self.store.user_data.children.items()))

            for name, child in self.store.user_data.children.items():
                if name in self.child_ids:
                    child.id = self.child_ids[name]
                    self.is_store_updated = True
        else:
            # Ids weren't parsed because all children in the persistant store
            # had an id saved already. Copy these values into self.child_ids
            for name, child in self.store.user_data.children.items():
                self.child_ids[name] = child.id

    @poll_on_method
    def collect_available_dates(self):
        self.available_dates = self.parser.get_available_dates(self.browser.html)

        self.logger.debug("available dates {}".format(self.available_dates))

    @poll_on_method
    def collect_available_times(self):
        self.available_times = []

        formatted_times = self.parser.get_available_times(self.browser.html)
        self.logger.debug("formatted times {}".format(formatted_times))
        self.available_times.extend([datetime(year=self.appt.datetime.year,
                                              month=self.appt.datetime.month,
                                              day=self.appt.datetime.day,
                                              hour=int(int(time) / 60),
                                              minute=int(time) % 60)
                                     for time in formatted_times])

    def select_children(self):
        for child in self.appt.children:
            self.check_child_id(self.child_ids[child])

    @poll_on_method
    def check_child_id(self, child_id):
        try:
            self.browser.check(child_id)
        except Exception as ex:
            raise SelectChildrenError(ex)

    @poll_on_method
    def select_date(self, date):
        try:
            self.browser.click_link_by_text(date.day)
        except Exception as ex:
            raise SelectDateError(f'{ex}: {date}')

    @poll_on_method
    def select_time(self):
        try:
            # Format the time with leading 0s stripped and lowercase am/pm
            time_string = self.appt.datetime.strftime('%I').lstrip('0') + \
                          self.appt.datetime.strftime(':%M') + \
                          self.appt.datetime.strftime('%p').lower()
            xpath = "//tr[td='{}']/td/form[@name='gridSubmitForm']/a".format(time_string)
            self.browser.find_by_xpath(xpath).click()
        except Exception as ex:
            raise SelectTimeError(ex)

    @poll_on_method
    def finalize_appointment(self):
        try:
            self.browser.find_by_name('finalize_appt').click()
        except Exception as ex:
            raise FinalizeError(ex)

    @poll_on_method
    def verify_appointment(self):
        link_text = self.appt.datetime.strftime('%A, %B ') + \
                    self.appt.datetime.strftime('%d').lstrip('0') + \
                    self.appt.datetime.strftime(', %Y at ') + \
                    self.appt.datetime.strftime('%I').lstrip('0') + \
                    self.appt.datetime.strftime(':%M') + \
                    self.appt.datetime.strftime('%p').lower()

        if not self.browser.find_link_by_partial_text(link_text):
            raise VerifyError(f'Cant find {link_text}')
