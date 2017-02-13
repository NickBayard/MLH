from datetime import datetime, date, timedelta, time
from enum import Enum
from collections import namedtuple


class ScheduleError(Exception):
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

    timeLimits = {WeekDay.MON: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                  WeekDay.TUE: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                  WeekDay.WED: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                  WeekDay.THU: TimeLimit(start=time(hour=8), stop=time(hour=20)),
                  WeekDay.FRI: TimeLimit(start=time(hour=8), stop=time(hour=18, minute=30)),
                  WeekDay.SAT: TimeLimit(start=time(hour=8), stop=time(hour=13)),
                  WeekDay.SUN: TimeLimit(start=time(hour=8), stop=time(hour=13))}

    @staticmethod
    def check_date(appt_start):
        if appt_start < datetime.now():
            # This appointment is past and needs to be purged
            # Should only be necessary to clean up appointments
            # that could not be successfully booked
            raise ScheduleError

        # check if the appointment is valid for today, tomorrow or
        # the next day.
        first_date = date.today()
        last_date = first_date + timedelta(days=2)
        appt_date = appt_start.date()

        return appt_date >= first_date and appt_date <= last_date

    @classmethod
    def check_time(cls, appt_start, duration):
        limit = cls.timeLimits[cls.WeekDay(appt_start.date().weekday())]

        appt_end = appt_start + timedelta(minutes=duration)

        return appt_start.time() >= limit.start and appt_end.time() <= limit.stop
