#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse
from datetime import datetime
from copy import copy

from version import __version__
from Persist import Persist
from PersistantData import Schedule
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
            args.dt = datetime.strptime(dt, '%Y%m%d %H%M')
        except:
            print('Unable to parse data and time of appointment.')
            args.date = args.time = None
            continue

        # Check that the appointment time slot is valid
        if ScheduleChecker.check_time(args.dt, args.duration):
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
    args.new_appt = False

    if args.children or args.date or args.time or args.duration:
        # User wants to schedule a new appointment
        args.new_appt = True

        # We need to make sure that all arguments are completed
        validate_children(args.children, persist)

        validate_duration(args.duration)

        validate_datetime(args)


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
                        choices=list(Appointment.durations.keys()), 
                        help='''Specfiy the duration of the appointment.''')
    parser.add_argument('-x', dest='clear', action='store_true', 
                        help='Clear appointments that have yet to be booked.')
    parser.add_argument('-l', dest='log_level', choices=['debug', 'info'], default='info',
                        help='log level')
    parser.add_argument('--execute', action='store_true',
                        help='Book appointments from the persistant store now')
    parser.add_argument('-p', dest='print_store', action='store_true',
                        help='Print the contents of the persistant store')

    return parser.parse_args()


def configure_logging(log_level):
    logger = logging.getLogger('mlh_logger')

    log_level = getattr(logging, log_level.upper(), None)
    logger.setLevel(log_level)

    fh = logging.FileHandler('log')
    sh = logging.StreamHandler()

    fileFormatter = logging.Formatter('%(asctime)s[%(levelname)s]<%(name)s>|%(funcName)s:%(message)s')
    streamFormatter = logging.Formatter('%(funcName)s:%(message)s')

    fh.setFormatter(fileFormatter)
    sh.setFormatter(streamFormatter)
    
    logger.addHandler(fh)
    logger.addHandler(sh)

def main(args):
    configure_logging(args.log_level)

    persist = Persist('db.pick')

    store = persist.get_data()

    if args.print_store:
        print(store)
        return

    if args.clear:
        store.appointments.clear() 
        persist.set_data()
        return

    validate_args(args, store)

    if args.new_appt:  # We want to schedule a new appointment
        # If an appointment was specified with children and infants,
        # it needs to be split into separate appointments
        appts = split_appointments(store, args)

        # Remove appointments that already exist in the store
        for appt in store.appointments:
            for new_appt in copy(appts):
                if new_appt == appt:
                    appts.remove(new_appt)

        store.appointments.extend(appts)

        persist.set_data()

    # book all available scheduled appointments
    if args.execute:
        handler = AppointmentHandler(persist)
        handler.run()


if __name__ == '__main__':
    main(parse_args())
