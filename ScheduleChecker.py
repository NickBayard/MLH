#! /usr/bin/env python3

from datetime import datetime, timedelta, time
from enum import Enum
from collections import namedtuple

class ScheduleError(exception):
    pass

class ScheduleChecker:
    """ This class maintains a list of times which can potentially be
    booked.  It takes a date as it's initialing parameter and can then
    validate additional dates to see if they can potentially be booked
    at this time."""
    
    # Child sitting hours
    # Mon-Thurs 8am-8pm
    # Fri       8am-630pm
    # Sat-Sun   8am-1pm
    class WeekDay(Enum):
        MON = 0
        TUE = 1
        WED = 2
        THU = 3
        FRI = 4
        SAT = 5
        SUN = 6

    TimeLimit = namedtuple('TimeLimit', ['start', 'stop'])

    timeLimits = { WeekDay.MON: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                   WeekDay.TUE: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                   WeekDay.WED: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                   WeekDay.THU: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                   WeekDay.FRI: TimeLimit(start=time(hour=8), stop=time(hour=18, minute=30)),
                   WeekDay.SAT: TimeLimit(start=time(hour=8), stop=time(hour=13)),
                   WeekDay.SUN: TimeLimit(start=time(hour=8), stop=time(hour=13))}

    def __init__(self):
        self.now = datetime.now() 

        self.weekday = WeekDay(self.now.date().weekday())

        #Calculate limits from this date
        last_book_date = now.date() + timedelta(days=2)

    def get_limits(self, wd):
        return self.timeLimits[WeekDay(wd % 7)]

    def check(self, appt_start, duration):
        if appt_start < now:
            # This appointment is past and needs to be purged
            # Should only be necessary to clean up appointments
            # that could not be successfully booked
            raise ScheduleError
        
        # get the child appointment boundary times for today, tomorrow, and 
        # the next day as these should all be available for booking
        limits = []
        for day in range(self.weekday, self.weekday + 3):
            limits.append(self.get_limits(day))

        appt_end = appt_start + timedelta(minutes=duration)

        if (appt_start >= limits[0].start and appt_end <= limits[0].stop) or
           (appt_start >= limits[1].start and appt_end <= limits[1].stop) or
           (appt_start >= limits[2].start and appt_end <= limits[2].stop):
            return True
        else:
            return False
