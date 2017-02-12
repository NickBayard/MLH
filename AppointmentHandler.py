#from Persist import *
from Appointment import Appointment
from ScheduleChecker import ScheduleChecker, ScheduleError
from copy import copy

class AppointmentHandler:
    """ AppointmentHandler takes an Appointment instance and runs it.
    The handler is responsible for handling exceptions that occur while
    trying to book the appointment and taking the appropriate actions."""

    def __init__(self, persist):
        self.persist = persist
        self.store = self.persist.get_data()
        self.appointments = self.store.appointments

    def handle_error(self, error):
        pass

    def handle_result(self, result):
        pass

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
                self.appointments.pop(i)
                
        appt = Appointment(self.store, schedule)

        for result, error in appt.book():
            if error:
                self.handle_error(error)
            elif result:
                self.handle_result(result)

        if self.appt.update_store():
            self.persist.set_data()
            self.store = self.persist.get_data()
