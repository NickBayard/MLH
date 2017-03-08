import logging
from copy import copy

from Appointment import Appointment, AppointmentError
from Appointment import LoginError, DurationError, ChildTypeError
from Appointment import SelectDateError, SelectTimeError, FinalizeError
from Appointment import UnableToBookAppointmentError
from ScheduleChecker import ScheduleChecker, ScheduleError
from Parser import ParseError, ParseCustomerIdError
from Parser import ParseChildIdError, ParseAvailableDatesError


class AppointmentHandler:
    """ AppointmentHandler takes an Appointment instance and runs it.
    The handler is responsible for handling exceptions that occur while
    trying to book the appointment and taking the appropriate actions."""

    def __init__(self, persist):
        self.persist = persist
        self.store = self.persist.get_data()
        self.appointments = self.store.appointments

    def handle_error(self, error):
        logging.debug('Failed due to {}'.format(error))
        self.appt.close()
        raise error

    def handle_result(self, result):
        # FIXME
        logging.debug('Success {}'.format(result))

    def run(self):
        # Copy items in appointments that can possibly be booked
        # at this time into schedule
        schedule = []
        for index, appt in enumerate(copy(self.appointments)):
            # Filter out appointments that aren't within reasonable hours
            try:
                if ScheduleChecker.check_date(appt.datetime):
                    schedule.append(appt)
            except ScheduleError:
                # This appointment has passed.  Purge from the list
                self.appointments.pop(index)

        self.appt = Appointment(self.store, schedule)

        for result in self.appt.book():
            if issubclass(type(result), AppointmentError) or issubclass(type(result), ParseError):
                self.handle_error(result)
            else:
                self.handle_result(result)

        self.appt.close()

        if self.appt.update_store():
            self.persist.set_data()
            self.store = self.persist.get_data()
