#! /usr/bin/env python3

from Persist import *
from Appointment import Appointment

class AppointmentHandler:
    """ AppointmentHandler takes an Appointment instance and runs it.
    The handler is responsible for handling exceptions that occur while
    trying to book the appointment and taking the appropriate actions."""

    def __init__(self, schedule, persist):
        self.schedule = schedule
        self.persist = persist

    def run(self)::
        # TODO determine if we need to book multiple appointments
        # (e.g. child + infant)
        self.appt.book()
        if self.appt.update_store():
            self.persist.set_data()
