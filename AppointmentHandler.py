import pdb
import logging
from copy import copy

from Appointment import Appointment, AppointmentError
from Appointment import LoginError, DurationError, ChildTypeError
from Appointment import SelectDateError, SelectTimeError, FinalizeError
from Appointment import UnableToBookAppointmentError, VerifyError
from ScheduleChecker import ScheduleChecker, ScheduleError
from Parser import ParseError, ParseChildIdError, ParseAvailableDatesError


class AppointmentHandler:
    """ AppointmentHandler takes an Appointment instance and runs it.
    The handler is responsible for handling exceptions that occur while
    trying to book the appointment and taking the appropriate actions."""

    def __init__(self, persist):
        self.persist = persist
        self.store = self.persist.get_data()
        self.appointments = self.store.appointments

    def handle_error(self, error, appt=None):
        logging.info('Appointment {} failed : {}'.format(appt, error))

    def handle_result(self, result, appt):
        # TODO Send an email/text

        logging.info('Booked appointment {}'.format(appt))

        for store_appt in copy(self.store.appointments):
            if store_appt == appt:
                self.store.appointments.remove(appt)

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

        try:
            for result, appt in self.appt.book():
                if issubclass(type(result), AppointmentError) or issubclass(type(result), ParseError):
                    self.handle_error(result, appt)
                else:
                    self.handle_result(result, appt)
        except Exception as ex:
            self.handle_error(ex)

        # There are several instances in which we need to update the persistant store.
        # Rather than attemp to track them all, just update the store each time regardless.
        self.persist.set_data()
        self.store = self.persist.get_data()
