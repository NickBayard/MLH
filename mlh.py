#! /usr/bin/env python3

import pdb
import argparse
from Persist import *
from Appointment import Appointment
from version import __version__
from Utils import error
from datetime import datetime

def validate_args(args, persist):
    if args.children and (not args.date or not args.time or not args.duration):
        error('''An appointment requires at least one child, a date, a time, and
            a duration.''')

    # Children should contain child info from persistant data
    for child in args.children:
        if child not in persist.user_data.children:
            error('{} not a valid child name')

    args.children = {child:persist.user_data.children[child] for child in args.children}

    # Combine args.data and args.time into a DateTime object
    dt = '{} {}'.format(args.date, args.time)
    try:
        args.dt = datetime.strptime(dt, '%Y%m%D %H%M')
    except:
        error('Unable to parse data and time of appointment')

    if args.duration not in Appointment.durations:
        error('Appointment duration must be either {} minutes'.format(
            ', '.join([str(dur) for dur in Appointment.durations.keys()])))

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
    
    else: 
        if args.children: # We want to book this appointment immediately
            appt = Schedule(datetime=args.dt, children=args.children, duration=args.duration)
            Appointment(store, appt)
        else: # book all available scheduled appointments
            for appt in store.appointments:
                Appointment(store, appt)


if __name__ == '__main__':
    main(parse_args())
