import pdb
import logging
from time import sleep
from datetime import datetime, timedelta

from splinter import Browser

from Parser import Parser, ParseChildIdError, ParseAvailableDatesError

class AppointmentError(Exception):
    pass


class LoginError(AppointmentError):
    pass


class DurationError(AppointmentError):
    pass


class ChildTypeError(AppointmentError):
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

    def book(self):
        first_pass = True
        RETRY_COUNT = 5

        self.browser.visit(self.url)

        try:
            self.login()
        except Exception as ex:
            raise ex

        for self.appt in self.appointments:
            logging.info("Booking appointment\n{}".format(self.appt))
            retry = 0
            while retry < RETRY_COUNT:
                try:
                    self.set_duration()
                    self.select_child_type()
                    self.collect_child_ids()

                    self.collect_available_dates()

                    if self.appt.datetime.date() in self.available_dates:
                        self.select_date(self.appt.datetime)
                    else:
                        raise UnableToBookAppointmentError

                    self.collect_available_times()
                    if self.appt.datetime in self.available_times:
                        self.select_time()
                        self.finalize_appointment()
                        self.verify_appointment()

                        # Successfully booked appointment
                        yield True, self.appt
                        break # from While retry loop
                    else:
                        raise UnableToBookAppointmentError

                except Exception as ex:
                    if ex is UnableToBookAppointmentError or retry >= RETRY_COUNT:
                        yield ex, self.appt
                        break # from While retry loop
                    else:
                        retry += 1

        # All appointments have been iterated through
        self.close()

    def update_store(self):
        return self.is_store_updated

    def login(self):
        logging.info("enter")

        try:
            self.browser.fill('loginname', self.store.user_data.user)
            self.browser.fill('password', self.store.user_data.password)
            self.browser.find_by_value('Log In').click()
        except:
            raise LoginError

    def close(self):
        self.browser.click_link_by_partial_href('logout')
        sleep(2)
        self.browser.quit()

    def set_duration(self):
        logging.info("enter")
        try:
            self.browser.find_by_name('service_id').select(self.durations[self.appt.duration])
        except:
            raise DurationError

    def select_child_type(self):
        logging.info("enter")
        child_types = {
            'child': '782',
            'infant': '783'}

        try:
            # Grab the first child name from the appointment list and use that
            # as the key to the user_data.children dictionary to look up the type
            pdb.set_trace()
            child_type = self.store.user_data.children[self.appt.children[0]].type
            self.browser.find_by_name('e_id').select(child_types[child_type])
            sleep(5)  # We need to give the page time to build
        except:
            raise ChildTypeError

    def collect_child_ids(self):
        logging.info('enter')
        self.child_ids = {}
        ids_were_parsed = False
        for name, child in self.store.user_data.children.items():
            if not child.id:
                self.child_ids = self.parser.get_child_ids(self.browser.html)
                ids_were_parsed = True
                break

        if ids_were_parsed:
            logging.debug('child_ids : {}'.format(self.child_ids))
            logging.debug('persitant child_ids : {}'.format(
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

    def collect_available_dates(self):
        logging.info("enter")
        self.available_dates = self.parser.get_available_dates(self.browser.html)

        logging.debug("available dates {}".format(self.available_dates))

    def collect_available_times(self):
        self.available_times = []

        sleep(6)

        formatted_times = self.parser.get_available_times(self.browser.html)
        logging.debug("date {} formatted times {}".format(date, formatted_times))
        self.available_times.extend([datetime(year=self.appt.datetime.year,
                                                month=self.appt.datetime.month,
                                                day=self.appt.datetime.day,
                                                hour=int(int(time) / 60),
                                                minute=int(time) % 60)
                                        for time in formatted_times])

    def select_date(self, date):
        logging.info("{}".format(date))

        try:
            for child in self.appt.children:
                self.browser.check(self.child_ids[child])

            self.browser.click_link_by_text(date.day)
        except:
            raise SelectDateError(date)

    def select_time(self):
        logging.info("enter")
        try:
            # Format the time with leading 0s stripped and lowercase am/pm
            time_string = self.appt.datetime.strftime('%I').lstrip('0') + \
                          self.appt.datetime.strftime(':%M') + \
                          self.appt.datetime.strftime('%p').lower()
            xpath = "//tr[td='{}']/td/font/form[@name='gridSubmitForm']/a".format(time_string)
            self.browser.find_by_xpath(xpath).click()
        except:
            raise SelectTimeError

    def finalize_appointment(self):
        try:
            sleep(2)
            self.browser.find_by_name('finalize_appt').click() 
        except:
            raise FinalizeError

    def verify_appointment(self):
        link_text = self.appt.datetime.strftime('%A, %B ') + \
                    self.appt.datetime.strftime('%d').lstrip('0') + \
                    self.appt.datetime.strftime(', %Y at %I:%M') + \
                    self.appt.datetime.strftime('%p').lower()

        sleep(2)

        if not self.browser.find_link_by_partial_text(link_text):
            raise VerifyError
