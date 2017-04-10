# -*- coding: utf-8 -*-

import sys
import logging
from collections import namedtuple
from datetime import datetime, timedelta, time
from PyQt5 import QtWidgets, QtGui, QtCore

from mainwindow import Ui_MainWindow
from ScheduleChecker import ScheduleChecker
from PersistantData import Schedule

TimeItem = namedtuple('TimeItem', ['timestr', 'dt'])

class mlhWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, mlh, children, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.backend = mlh
        self.logger = logging.getLogger('mlh_logger')

        #init children list
        self.selected_children = None
        self.listWidget.addItems(children)
        self.listWidget.itemSelectionChanged.connect(self.set_children)

        #init calendar and time/combobox
        self.selected_time = None
        self.set_date()
        self.calendarWidget.selectionChanged.connect(self.set_date)
        self.comboBox.currentIndexChanged.connect(self.set_time)

        #init duration
        self.set_duration()
        self.spinBox.valueChanged.connect(self.set_duration)

        self.pushButton.clicked.connect(self.add_appointment)

    def set_children(self):
        self.selected_children = [item.text() for item in self.listWidget.selectedItems()]
        self.logger.debug("New children : {}".format(self.selected_children))

    def set_duration(self):
        self.selected_duration = self.spinBox.value()
        self.logger.debug("New duration : {}".format(self.selected_duration))

    def set_time(self, index):
        self.selected_time = self.comboBoxItems[index]
        self.logger.debug("New time : {}".format(self.selected_time.dt))

    def set_date(self):
        # TODO covert selected date to datetime
        date = self.calendarWidget.selectedDate()
        self.selected_date = datetime(year=date.year(),
                                      month=date.month(),
                                      day=date.day())

        self.logger.debug("New date : {}".format(self.selected_date))

        # Update times in combobox

        weekday = ScheduleChecker.WeekDay(self.selected_date.weekday())

        time_limit = ScheduleChecker.timeLimits[weekday]

        start = datetime(year=self.selected_date.year,
                         month=self.selected_date.month,
                         day=self.selected_date.day,
                         hour=time_limit.start.hour,
                         minute=time_limit.start.minute)

        stop = datetime(year=self.selected_date.year,
                         month=self.selected_date.month,
                         day=self.selected_date.day,
                         hour=time_limit.stop.hour,
                         minute=time_limit.stop.minute)
        self.comboBoxItems = []

        while start <= stop:
            timestamp = start.strftime("%I:%M%p")
            self.comboBoxItems.append(TimeItem(timestamp, start))
            # The dict keys are the index of list items
            start += timedelta(minutes=30)

        # Set the comboBox selected index
        # If there was a previously selected time, use that. Otherwise, default to 9am
        timestamp = self.selected_time.timestr if self.selected_time else "09:00AM"

        new_index = 0
        for index, timeItem in enumerate(self.comboBoxItems):
            if timeItem.timestr == timestamp:
                new_index = index
                break

        self.comboBox.clear()
        self.comboBox.addItems([item.timestr for item in self.comboBoxItems])
        self.comboBox.setCurrentIndex(new_index)

    def add_appointment(self):
        self.backend.add_appointment(Schedule(datetime=self.selected_time.dt,
                                              duration=self.selected_duration,
                                              children=self.selected_children))


class mlhGui():
    def __init__(self, mlh, children):
        app = QtWidgets.QApplication(sys.argv)
        window = mlhWindow(mlh, children)
        window.show()
        app.exec_()
