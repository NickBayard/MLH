import pickle
from pathlib import Path
from getpass import getpass
import re
from Utils import int_input, input_with_quit
from PersistantData import PersistantData, UserData, Child


class Persist:
    """Persist is in charge of managing the PersistantData class instance
    including pickling and un-pickling the file.  It is also responsible for
    populating the contents of the PersistantData instance the first time that
    it is created by prompting the user."""

    def __init__(self, path):
        self.file = Path(path)

        # TODO get directory of python script
        if not self.file.exists():
            self._populate_user_data()
            self.set_data()
        else:
            with self.file.open('rb') as f:
                self.store = pickle.load(f)

    def _get_username(self):
        while True:
            user = input_with_quit('Enter your email/username: ')
            m = re.match("^[a-zA-Z0-9-.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,3}$", user)
            if not m:
                print('Email is not valid.  Please try again.')
            else:
                break

        return m.group(0)

    def _get_password(self):
        while True:
            password = getpass('Enter your password: ')
            password2 = getpass('Enter your password again: ')
            if password != password2:
                print('Passwords do not match.  Please try again.')
            else:
                break
        return password

    def _get_children(self):
        count = int_input('How many children do you have? ', 1, 20)

        children = {}
        for child in range(count):
            name = input_with_quit('Please enter the name for child {}: '.format(child + 1))
            name = name[0].upper() + name[1:].lower()
            while True:
                type = input_with_quit('Is {} a child or infant? (c/i) '.format(name))
                type = type.lower()[0]
                if type not in ['c', 'i']:
                    print("Sorry I don\'t understand your answer.")
                else:
                    type = 'child' if type == 'c' else 'infant'
                    if type == 'infant':
                        name = '{}18'.format(name)
                    break
            children[name] = Child(type)

        return children

    def _populate_user_data(self):
        print("This looks like the first time that you've used Mother's Little Helper.\n")
        print('Please fill out some information that will help me book your future appointments.\n')

        self.store = PersistantData(UserData(user=self._get_username(),
                                             password=self._get_password(),
                                             children=self._get_children()))

    def get_data(self):
        return self.store

    def set_data(self):
        with self.file.open('wb') as f:
            pickle.dump(self.store, f)
