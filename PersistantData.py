
class UserData:
    def __init__(self, user, password, children={}):
        self.user = user
        self.password = password
        self.children = children


class Child:
    def __init__(self, t, id=None):
        self.type = t
        self.id = id


class Schedule:
    def __init__(self, datetime, duration, children=[]):
        self.datetime = datetime
        self.duration = duration
        self.children = children


class PersistantData:
    """PersistantData contains the data structure containing information 
    about the user account, the children and the appointents that should
    be booked in the future.  This class gets pickled for persistance."""

    def __init__(self, user_data, appointments=[]):
        self.user_data = user_data #UserData
        self.appointments = appointments #list  of Schedule

