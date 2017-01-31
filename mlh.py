#! /usr/bin/env python3

import pdb
import argparse
from Persist import *
from Appointment import Appointment
from version import __version__
from Utils import *
from datetime import datetime

def validate_children(children, persist):
    if type(children) not list:
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
            break
        except:
            print('Unable to parse data and time of appointment.')
            args.date = args.time = None

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
    if args.execute: 
        if not args.children and not args.date and not args.time and not args.duration:
            # User wants to book appointments in persistant store
            return

    # User wants to book a specific appointment
    # We need to make sure that all arguments are completed
    validate_children(args.children, persist)

    validate_datetime(args)

    validate_duration(args.duration)

    return args

def parse_args():
    parser = argparse.ArgumentParser(
                description='''Utility for advanced booking of child sitting 
                appointments at Paul Derda Recreation Center''')

    parser.add_argument('-v', '--version', action='version', 
        version="Mother's Little Helper {}".format(__version__))
    parser.add_argument('-e', '--execute', action='store_true', 
        help='''When specified without any additional parameters, book all
        available appointments that have been scheduled.  When specified
        with parameters, book only the specified appointment.''')
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
    p = Persist('mlh.pick')

    store = p.get_data()

    args = validate_args(args, store)

    if not args.execute: # We want to schedule an appointment
        store.appointments.append(Schedule(datetime=args.dt, children=args.children)) 
        p.set_data()
    
    else: 
        if args.children: # We want to book this appointment immediately
            appt = Schedule(datetime=args.dt, children=args.children, duration=args.duration)
            Appointment(store, appt)
        else: # book all available scheduled appointments
            for appt in store.appointments:
                try:
                    book = Appointment(store, appt)
                    if book.update_store():
                        p.set_data()
                except RuntimeError:
                    pass


if __name__ == '__main__':
    main(parse_args())
