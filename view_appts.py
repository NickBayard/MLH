# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_appts.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewAppointments(object):
    def setupUi(self, ViewAppointments):
        ViewAppointments.setObjectName("ViewAppointments")
        ViewAppointments.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ViewAppointments)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.removeAppointmentsButton = QtWidgets.QPushButton(ViewAppointments)
        self.removeAppointmentsButton.setObjectName("removeAppointmentsButton")
        self.horizontalLayout.addWidget(self.removeAppointmentsButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.appointmentList = QtWidgets.QListWidget(ViewAppointments)
        self.appointmentList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.appointmentList.setObjectName("appointmentList")
        self.verticalLayout.addWidget(self.appointmentList)

        self.retranslateUi(ViewAppointments)
        QtCore.QMetaObject.connectSlotsByName(ViewAppointments)

    def retranslateUi(self, ViewAppointments):
        _translate = QtCore.QCoreApplication.translate
        ViewAppointments.setWindowTitle(_translate("ViewAppointments", "View Appointments"))
        self.removeAppointmentsButton.setText(_translate("ViewAppointments", "Remove"))

