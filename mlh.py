#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import argparse
from datetime import datetime
from version import __version__
from Persist import Persist
from Appointment import Appointment
from Utils import int_input, input_with_quit
from AppointmentHandler import AppointmentHandler
from ScheduleChecker import ScheduleChecker


def validate_children(children, persist):
    if type(children) is not list:
        raise TypeError

    if not children:
        count = int_input('How many children would you like to book? ', 1, 20)

        for child in range(count):
            while True:
                name = input_with_quit('Please enter the name for child {}'.format(child + 1))
                if name not in persist.user_data.children:
                    print('{} not a valid child name'.format(name))
                else:
                    break

            children.append(name)


def validate_datetime(args):
    while True:
        if not args.date:
            args.date = input_with_quit('Please enter the date you would like to book (YYYYMMDD): ')

        if not args.time:
            args.time = input_with_quit('Please enter the time you would like to book (HHMM): ')

        # Combine args.data and args.time into a DateTime object
        dt = '{} {}'.format(args.date, args.time)
        try:
            args.dt = datetime.strptime(dt, '%Y%m%D %H%M')
        except:
            print('Unable to parse data and time of appointment.')
            args.date = args.time = None
            continue

        # Check that the appointment time slot is valid
        if ScheduleChecker.check_time(args.datetime, args.duration):
            break
        else:
            print('The time {} on {} is not a valid appointment time.'.format(args.time, args.date))


def validate_duration(duration):
    duration_str = ', '.join([str(dur) for dur in Appointment.durations.keys()])
    while True:
        if not duration:
            duration = int_input('Please enter the duration of the appointment ({}): '.format(
                duration_str))

        if duration not in Appointment.durations:
            print('Appointment duration must be either {} minutes'.format(duration_str))
            duration = None
        else:
            break


def validate_args(args, persist):
    if not args.children and not args.date and not args.time and not args.duration:
        # User wants to book appointments in persistant store only
        return

    # User wants to book a specific appointment
    # We need to make sure that all arguments are completed
    validate_children(args.children, persist)

    validate_duration(args.duration)

    validate_datetime(args)

    args.new_appt = True

    return args


def split_appointments(store, args):
    appointments = []

    def get_appt_by_type(type):
        names = [name for name, info in store.user_data.children.items() 
                 if info.type == type and name in args.children]

        if names:
            appointments.append(Schedule(datetime=args.dt, duration=args.duration, children=names))

    get_appt_by_type('child')
    get_appt_by_type('infant')

    return appointments


def parse_args():
    parser = argparse.ArgumentParser(
                description='''Utility for advanced booking of child sitting
                appointments at Paul Derda Recreation Center''')

    parser.add_argument('-v', '--version', action='version',
                        version="Mother's Little Helper {}".format(__version__))
    parser.add_argument('-c', dest='children', nargs='+', metavar='CHILD',
                        help='''List the names of the children for this appointment.''')
    parser.add_argument('-d', dest='date', metavar='YYYYMMDD',
                        help='''Specify the date to book.''')
    parser.add_argument('-t', dest='time', metavar='HHMM',
                        help='''Specify the time to book.  HH is 00-23.''')
    parser.add_argument('-r', dest='duration', metavar='MINUTES', type=int,
                        default=90, help='''Specfiy the duration of the appointment.''')

    return parser.parse_args()


def main(args):
    pdb.set_trace()
    persist = Persist('mlh.pick')

    store = persist.get_data()

    args = validate_args(args, store)

    if args.new_appt:  # We want to schedule a new appointment
        # If an appointment was specified with children and infants,
        # it needs to be split into separate appointments
        for sched in split_appointments(store, args):
            store.appointments.append(sched)

        persist.set_data()

    # book all available scheduled appointments
    handler = AppointmentHandler(persist)
    handler.run()


if __name__ == '__main__':
    main(parse_args())
