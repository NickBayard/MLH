
class UserData:
    def __init__(self, user, password, children={}):
        self.user = user
        self.password = password
        # Dict of Child with child's name as the key
        self.children = children  

    def __str__(self):
        children = ''.join(['   {}:\n{}'.format(name, child) for name, child in self.children.items()])
        return ' UserData:\n  user: {}\n  children:\n{}'.format(self.user, children)


class Child:
    def __init__(self, t, id=None):
        self.type = t
        self.id = id

    def __str__(self):
        return '    type: {}\n    id: {}\n'.format(self.type, self.id)


class Schedule:
    def __init__(self, datetime, duration, children=[]):
        self.datetime = datetime
        self.duration = duration
        self.children = children

    def __eq__(self, other):
        return self.datetime == other.datetime and self.children == other.children

    def __str__(self):
        children = ', '.join(['{}'.format(child) for child in self.children])
        return '  datetime: {}\n  duration: {}\n  children: {}\n'.format(
               self.datetime, self.duration, children)


class PersistantData:
    """PersistantData contains the data structure containing information
    about the user account, the children and the appointents that should
    be booked in the future.  This class gets pickled for persistance."""

    def __init__(self, user_data, appointments=[]):
        self.user_data = user_data  # UserData
        self.appointments = appointments  # list  of Schedule

    def __str__(self):
        appointments = '\n'.join(['{}'.format(appt) for appt in self.appointments])
        return 'PersistantData:\n{} Appointments:\n{}'.format(self.user_data,
               appointments)
