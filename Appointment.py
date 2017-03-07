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

        self.browser.visit(self.url)

        try:
            self.login()
        except LoginError:
            return LoginError
        except ParseCustomerIdError:
            return ParseCustomerIdError

        for self.appt in self.appointments:
            try:
                self.set_duration()
            except DurationError:
                yield DurationError
                continue

            try:
                self.select_child_type()
            except ChildTypeError:
                yield ChildTypeError
                continue

            try:
                self.collect_child_ids()
            except ParseChildIdError:
                yield ParseChildIdError
                continue

            if first_pass:
                first_pass = False
                try:
                    self.collect_available_times()
                except ParseAvailableDatesError:
                    yield ParseAvailableDatesError
                except SelectDateError:
                    yield SelectDateError

            logging.debug("available times")
            logging.debug(self.available_times)
            logging.debug("appt {}".format(self.appt.datetime))

            if self.appt.datetime in self.available_times:
                try:
                    self.select_date(self.appt.datetime)
                except SelectDateError:
                    yield SelectDateError
                    continue

                try:
                    self.select_time()
                except SelectTimeError:
                    yield SelectTimeError
                    continue

                try:
                    pass
                    #self.finalize_appointment()
                except FinalizeError:
                    yield FinalizeError
                    continue
            else:
                yield UnableToBookAppointmentError

            # TODO verify that appointment link is present
            # Successfully booked appointment
            self.close()
            yield True

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
        sleep(1)
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
            child_type = self.store.user_data.children[self.appt.children[0]].type
            self.browser.find_by_name('e_id').select(child_types[child_type])
            sleep(5)  # We need to give the page time to build
        except:
            raise ChildTypeError

    def collect_child_ids(self):
        logging.info('enter')
        self.child_ids = None
        for name, child in self.store.user_data.children.items():
            if not child.id:
                self.child_ids = self.parser.get_child_ids(self.browser.html)
                break

        if self.child_ids:
            logging.debug('child_ids : {}'.format(self.child_ids))
            logging.debug('persitant child_ids : {}'.format(
                          self.store.user_data.children.items()))

            for name, child in self.store.user_data.children.items():
                if name in self.child_ids:
                    child.id = self.child_ids[name]
                    self.is_store_updated = True

    def collect_available_times(self):
        logging.info("enter")
        available_dates = self.parser.get_available_dates(self.browser.html)

        logging.debug("available dates {}".format(available_dates))
        self.available_times = []

        for date in available_dates:
            self.select_date(date)
            sleep(6)

            formatted_times = self.parser.get_available_times(self.browser.html)
            logging.debug("date {} formatted times {}".format(date, formatted_times))
            self.available_times.extend([datetime(year=date.year,
                                                  month=date.month,
                                                  day=date.day,
                                                  hour=int(int(time) / 60),
                                                  minute=int(time) % 60)
                                         for time in formatted_times])

    def select_date(self, date):
        logging.info("{}".format(date))

        for child in self.appt.children:
            self.browser.check(self.child_ids[child])

        try:
            self.browser.click_link_by_text(date.day)
        except:
            raise SelectDateError(date)

    # TODO Do this thing
    def select_time(self):
        logging.info("enter")
        try:
            # TODO The time needs to be selected with xpath
            pass
        except:
            raise SelectTimeError

    # TODO Do this thing
    def finalize_appointment(self):
        try:
            pass
        except:
            raise FinalizeError
