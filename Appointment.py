import sys
import requests
from datetime import datetime
from datetime import date as datedate
from Parser import Parser
from Utils import *

class Appointment:
    """The Appointment is the workhorse of this application.  It will
    attempt to book a child sitting appointment  or appointments at 
    the specified time while providing feedback to the AppointmentHandler
    should there be any issues with making the booking."""

    url = 'https://booknow.appointment-plus.com/73kgtt5s/'

    post_data = {
        'id' : '330',
        'location_id' : '330',
        'headquarters_id' : '330',
        'd' : 'appointplus356',
        'page' : '10',
        'm' : '2',
        'type' : '23',
        'action' : 'log_in',
        'e_id' : ''}

    durations = {
        30: '973',
        60: '974',
        90: '975'}

    def __init__(self, store, appt):
        self.session = requests.Session()
        self.parser = Parser()

        self.store = store
        self.is_store_updated = False
        self.appoinment = appt

    def book(self):
        self.login()
        self.set_duration()
        self.select_child_type()
        self.select_date()
        self.select_time()
        self.finalize_appointment()

        #TODO verify that appointment link is present

    def update_store(self):
        return self.is_store_updated

    def post(self, data, update=True):
        if update:
            self.post_data.update(data)

        r = self.session.post(self.url, data=self.post_data if update else data)

        r.raise_for_status()

        self.text = r.text

    def login(self):
        login_data = {
            'login_screen' : 'yes',
            'loginname' : self.store.user_data.user,
            'password' : self.store.user_data.password}

        login_data.update(self.post_data)

        try:
            self.post(self.session, login_data, update=False)
        except:
            error('Unable to log in')

        try:    
            self.post_data['customer_id'] = self.parser.get_customeid(self.text)
        except:
            error('Could not parse customer id')

    def set_duration(self):
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
            'service_id': durations[self.appt.duration],
            'event': ''}
        try:
            self.post(self.session, duration_data, update=False)
        except:
            error('Unable to set duration of appointment')

    def select_child_type(self, child_type):
        child_types = {
            'child' : '782',
            'infant' : '783'}

        child_data = {'e_id' : child_types.get(child_type, child_types['child'])}

        try:
            self.post(self.session, child_data)
        except:
            error('Unable to set child type')

        for child in self.store.user_data.children:
            if not child.id:
                try:
                    self.child_ids = self.parser.get_child_ids(self.text)
                except:
                    error('Unable to parse child ids')

                for child in self.store.user_data.children:
                    if child.name in self.child_ids:
                        child.id = self.child_ids[child.name]
                        self.is_store_updated = True

                break

        try:
            self.available_dates = self.parser.get_available_dates(text,)
        except:
            error('No dates available for booking at this time')

    @staticmethod
    def surrounding_dates(date):
        format = '%Y%m%d'
        d = datetime.strptime(date, format)
        
        # calculate previous month
        year = d.year - 1 if d.month == 1 else d.year
        month = 12 if d.month == 1 else d.month - 1
        day = 1
        previous = datedate(year, month, day)

        #calculate next month
        year = d.year + 1 if d.month == 12 else d.year
        month = 1 if d.month == 12 else d.month + 1
        next = datedate(year, month, day)

        return previous.strftime(format), next.strftime(format)

    def select_date(self):
        # TODO use appt.dt
        date = self.available_dates[-1] #TODO book latest date for now
        prev_date, next_date = Appointment.surrounding_dates(date)

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
            'starting_date': date,
            'date_ymd': date} 

        for child in self.appt.children:
            date_data[child.id] = 'on'
        
        try:
            self.post(self.session, date_data)
        except:
            error('Unable to select date')

        #TODO the time needs to be specified using appt.dt
        try:
            self.time_data = self.parser.get_time_data(self.text)
        except:
            error('Unable to parse time data')
            
    def select_time(self):
        try:
            self.post(self.session, self.time_data, update=False)
        except:
            error('Unable to select time')

        try:
            self.final_data = self.parser.get_final_data(self.text)
        except:
            error('Unable to parse finalization data')

    def finalize_appointment(self):
        try:
            self.post(self.session, self.final_data, update=False)
        except:
            error('Unable to finalize appointment')

        with open('complete.html', 'w') as f:
            f.write(self.text)

