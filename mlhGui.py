# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtGui, QtCore

from mainwindow import Ui_MainWindow
from ScheduleChecker import ScheduleChecker
from PersistantData import Schedule

class mlhWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, mlh, children, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.backend = mlh

        self.listWidget.addItems(children)

        self.set_date()
        self.calendarWidget.selectionChanged.connect(self.set_date)

        # Initialize combobox
        self.comboBox.currentIndexChanged.connect(self.set_time)
        try:
            self.comboBox.setCurrentIndex(self.comboBoxItems.index("09:00AM"))
        except:
            self.comboBox.setCurrentIndex(0)

        self.set_duration()
        self.spinBox.valueChanged.connect(self.set_duration)

        self.pushButton.clicked.connect(self.add_appointment)

    def set_duration(self):
        self.selected_duration = self.spinBox.value()
        print("New duration : {}".format(self.selected_duration))

    def set_time(self, index):
        self.comboBoxIndex = index
        print("New time index : {}".format(self.comboBoxIndex))

    def set_date(self):
        self.selected_date = self.calendarWidget.selectedDate()
        print("New date : {}".format(self.selected_date))

        # Update times in combobox
        self.comboBox.clear()

        weekday = ScheduleChecker.WeekDay(self.selected_date.dayOfWeek() - 1)

        time_limit = ScheduleChecker.timeLimits[weekday]

        start = datetime(year=self.selected_date.year(),
                         month=self.selected_date.month(),
                         day=self.selected_date.day(),
                         hour=time_limit.start.hour,
                         minute=time_limit.start.minute)

        stop = datetime(year=self.selected_date.year(),
                         month=self.selected_date.month(),
                         day=self.selected_date.day(),
                         hour=time_limit.stop.hour,
                         minute=time_limit.stop.minute)
        self.comboBoxItems = []

        while start <= stop:
            self.comboBoxItems.append(start.strftime("%I:%M%p"))
            start += timedelta(minutes=30)

        self.comboBox.addItems(self.comboBoxItems)

    def add_appointment(self):
        #self.backend.add_appointment(Schedule())
        pass


class mlhGui():
    def __init__(self, mlh, children):
        app = QtWidgets.QApplication(sys.argv)
        window = mlhWindow(mlh, children)
        window.show()
        app.exec_()
