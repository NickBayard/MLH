# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets

from mainwindow import Ui_MainWindow
from ScheduleChecker import ScheduleChecker
from PersistantData import Schedule

class mlhWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, mlh, children, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.backend = mlh

        # Add children to list
        for child in children:
            self.listWidget.addItem(QtWidgets.QListWidgetItem(child))

        self.fill_times()
        self.calendarWidget.selectionChanged.connect(self.set_date)

        self.pushButton.clicked.connect(self.add_appointment)

    def set_date(self):
        self.selected_date = self.calendarWidget.selectedDate()
        self.fill_times()

    def fill_times(self):
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
        items = []

        while start <= stop:
            items.append(start.strftime("%I:%M%p"))
            start += timedelta(minutes=30)

        self.comboBox.addItems(items)

    def add_appointment(self):
        # TODO build datetime object and Scheudle object
        #self.backend.add_appointment(Schedule())
        pass


class mlhGui():
    def __init__(self, mlh, children):
        app = QtWidgets.QApplication(sys.argv)
        window = mlhWindow(mlh, children)
        window.show()
        app.exec_()
