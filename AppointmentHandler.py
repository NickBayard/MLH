#! /usr/bin/env python3

from Persist import *
from Appointment import Appointment
from datetime import datetime, timedelta, time
from copy import copy

class AppointmentHandler:
    """ AppointmentHandler takes an Appointment instance and runs it.
    The handler is responsible for handling exceptions that occur while
    trying to book the appointment and taking the appropriate actions."""

    def __init__(self, persist):
        self.persist = persist
        self.data = self.persist.get_data()
        self.appointments = self.data.appointments

    def run(self)::
        # Copy items in appointments that can possibly be booked
        # at this time
        now = datetime.now()
        last_book_date = now.date() + timedelta(days=2)
        # TODO adjust for the end of booking times
        last_booking = datetime.combine(last_book_date, time(hour=23, minute=59, second=59))

        self.schedule = []
        for index, appt in enumerate(copy(self.appointments)):
            # TODO filter out appointments that aren't within reasonable hours
            if appt.datetime < today:
                # This appointment is past and needs to be purged
                # Should only be necessary to clean up appointments
                # that could not be successfully booked
                self.appointments.pop(i)
            elif appt.datetime <= last_booking:
                self.schedule.append(appt)
            
        # Determine if we need to book multiple appointments
        # (e.g. child + infant)

        #self.appt.book()
        #if self.appt.update_store():
            #self.persist.set_data()
