# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from mainwindow import Ui_MainWindow
import ScheduleChecker

class mlhWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, mlh, children, parent=None):
        super().__init__(parent)
        self.setupUi(self) 

        # Add children to list
        for child in children:
            self.listWidget.addItem(QtWidgets.QListWidgetItem(child))

        date = seld.calendarWidget.selectedDate()
        self.fill_times(ScheduleChecker.timeLimits[date.dayOfWeek - 1])

class mlhGui():
    def __init__(self, mlh, children):
        app = QtWidgets.QtApplication
        window = mlhWindow(mlh, children)
        window.show()
        app.exec_()
