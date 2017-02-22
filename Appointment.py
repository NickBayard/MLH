import pdb
import requests
from datetime import datetime, timedelta

from Parser import Parser, ParseCustomerIdError, ParseChildIdError, ParseAvailableDatesError


class AppointmentError(Exception):
    pass


class LoginError(AppointmentError):
    pass


class DurationError(AppointmentError):
    pass


class ChildTypeError(AppointmentError):
    pass


class SelectDateError(AppointmentError):
    pass


class SelectTimeError(AppointmentError):
    pass


class UnableToBookAppointmentError(AppointmentError):
    pass


class FinalizeError(AppointmentError):
    pass


class Appointment:
    """The Appointment is the workhorse of this application.  It will
    attempt to book a child sitting appointment  or appointments at
    the specified time while providing feedback to the AppointmentHandler
    should there be any issues with making the booking."""

    url = 'https://booknow.appointment-plus.com/73kgtt5s/'

    durations = {
        30: '973',
        60: '974',
        90: '975'}

    def __init__(self, store, appointments):
        self.session = requests.Session()
        self.post_data = {
            'id': '330',
            'location_id': '330',
            'headquarters_id': '330',
            'd': 'appointplus356',
            'page': '10',
            'm': '2',
            'type': '23',
            'action': 'log_in',
            'e_id': ''}

        self.parser = Parser()

        self.store = store
        self.is_store_updated = False
        self.appointments = appointments

    def book(self):
        first_pass = True
        try:
            self.login()
        except LoginError:
            return LoginError
        except ParseCustomerIdError:
            return ParseCustomerIdError

        for self.appt in self.appointments:
            try:
                self.set_duration()
            except DurationError:
                yield DurationError
                continue

            try:
                self.select_child_type()
            except ChildTypeError:
                yield ChildTypeError
                continue

            # FIXME selecting the child type does not
            # return content with the child ids and checkboxes
            # Likely that the session isn't being stored
            try:
                self.collect_child_ids()
            except ParseChildIdError:
                yield ParseChildIdError
                continue

            if first_pass:
                first_pass = False
                try:
                    self.collect_available_times()
                except ParseAvailableDatesError:
                    yield ParseAvailableDatesError
                except SelectDateError:
                    yield SelectDateError

            if self.appt.datetime in self.available_times:
                try:
                    self.select_date()
                except SelectDateError:
                    yield SelectDateError
                    continue

                try:
                    self.select_time()
                except SelectTimeError:
                    yield SelectTimeError
                    continue

                try:
                    self.finalize_appointment()
                except FinalizeError:
                    yield FinalizeError
                    continue
            else:
                yield UnableToBookAppointmentError

            # TODO verify that appointment link is present
            # Successfully booked appointment
            yield True

    def update_store(self):
        return self.is_store_updated

    def post(self, data, update=True):
        if update:
            self.post_data.update(data)

        r = self.session.post(self.url, params=self.post_data if update else data)

        r.raise_for_status()

        print(r.url)
        print("data : {}".format(self.post_data if update else data))

        self.text = r.text

    def login(self):
        print("login")
        login_data = {
            'login_screen': 'yes',
            'loginname': self.store.user_data.user,
            'password': self.store.user_data.password}

        login_data.update(self.post_data)

        try:
            self.post(login_data, update=False)
        except:
            raise LoginError

        self.post_data['customer_id'] = self.parser.get_customer_id(self.text)

    def set_duration(self):
        print("set duration")
        duration_data = {
            'selection_form': 'yes',
            'wt_c_id': '',
            'wt_d': '',
            'auth': 'yes',
            'action2': '',
            'show_services': '',
            'temp_addon_id': '',
            'customer_location_id': '330',
            'vo': '',
            'selected_pets': '',
            'pet_count': '',
            'pet_list': '',
            'selected_children': '',
            'child_count': '',
            'children_list': '',
            'staff_switch_loc': '',
            'day_name': 'any',
            'rep_id': '',
            'service_id': self.durations[self.appt.duration],
            'event': ''}
        try:
            self.post(duration_data)
        except:
            raise DurationError

    def select_child_type(self):
        print("select_child_type")
        child_types = {
            'child': '782',
            'infant': '783'}

        # Grab the first child name from the appointment list and use that
        # as the key to the user_data.children dictionary to look up the type
        child_type = self.store.user_data.children[self.appt.children[0]].type
        child_data = {'e_id': child_types[child_type]}

        try:
            self.post(child_data)
        except:
            raise ChildTypeError

    def collect_child_ids(self):
        self.child_ids = None
        for name, child in self.store.user_data.children.items():
            if not child.id:
                self.child_ids = self.parser.get_child_ids(self.text)
                break

        if self.child_ids:
            for name, child in self.store.user_data.children.items():
                if name in self.child_ids:
                    child.id = self.child_ids[name]
                    self.is_store_updated = True

    def collect_available_times(self):
        available_dates = self.parser.get_available_dates(self.text)

        self.available_times = []

        for date in available_dates:
            self.select_date(date)
            formatted_times = self.parser.get_available_times(self.text)
            self.available_times.extend([datetime(year=date.year,
                                                  month=date.month,
                                                  day=date.month,
                                                  hour=int(time / 60),
                                                  minute=time % 60)
                                         for time in formatted_times])

    def select_date(self, date):
        print("select date")
        # Need first day of previous month)
        temp_date = datetime(year=date.year -1 if date.month == 1 else date.year, 
                             month=12 if date.month == 1 else date.month - 1, 
                             day=1)
        prev_date = temp_date.strftime('%Y%m%d')

        # Need first day of next month
        temp_date = datetime(year=date.year + 1 if date.month == 12 else date.year, 
                             month=1 if date.month == 12 else date.month + 1,
                             day=1)
        next_date = temp_date.strftime('%Y%m%d')

        this_date = date.strftime('%Y%m%d')

        date_data = {
            'action': 'viewappts',
            'new_child1_first_name': '',
            'new_child1_last_name': '',
            'new_child2_first_name': '',
            'new_child2_last_name': '',
            'previous_service_id': self.post_data['service_id'],
            'view_prev_month': '',
            'view_next_month': '',
            'next_date': next_date,
            'prev_date': prev_date,
            'starting_date': this_date,
            'date_ymd': this_date}

        for child in self.appt.children:
            date_data[self.child_ids[child]] = 'on'

        try:
            self.post(date_data)
        except:
            raise SelectDateError(date)

    # TODO Do this thing
    def select_time(self):
        print("select time")
        #try:
            #self.post(self.time_data, update=False)
        #except:
            #raise SelectTimeError

        #try:
            #self.final_data = self.parser.get_final_data(self.text)
        #except:
            #error('Unable to parse finalization data')

    # TODO Do this thing
    def finalize_appointment(self):
        try:
            self.post(self.final_data, update=False)
        except:
            raise FinalizeError

        with open('complete.html', 'w') as f:
            f.write(self.text)
