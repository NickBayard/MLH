# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets

from mainwindow import Ui_MainWindow
from ScheduleChecker import ScheduleChecker

class mlhWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, mlh, children, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Add children to list
        for child in children:
            self.listWidget.addItem(QtWidgets.QListWidgetItem(child))

        self.fill_times(self.calendarWidget.selectedDate())

    def fill_times(self, date):
        self.comboBox.clear()

        weekday = ScheduleChecker.WeekDay(date.dayOfWeek() - 1)

        time_limit = ScheduleChecker.timeLimits[weekday]

        start = datetime(year=date.year(),
                         month=date.month(),
                         day=date.day(),
                         hour=time_limit.start.hour,
                         minute=time_limit.start.minute)

        stop = datetime(year=date.year(),
                         month=date.month(),
                         day=date.day(),
                         hour=time_limit.stop.hour,
                         minute=time_limit.stop.minute)
        items = []

        while start <= stop:
            items.append(start.strftime("%I:%M%p"))
            start += timedelta(minutes=30)

        self.comboBox.addItems(items)

class mlhGui():
    def __init__(self, mlh, children):
        app = QtWidgets.QApplication(sys.argv)
        window = mlhWindow(mlh, children)
        window.show()
        app.exec_()
