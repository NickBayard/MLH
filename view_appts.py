# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_appts.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewAppointments(object):
    def setupUi(self, ViewAppointments):
        ViewAppointments.setObjectName("View")
        ViewAppointments.setWindowModality(QtCore.Qt.WindowModal)
        ViewAppointments.resize(737, 597)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ViewAppointments)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.removeApptButton = QtWidgets.QPushButton(ViewAppointments)
        self.removeApptButton.setObjectName("removeApptButton")
        self.horizontalLayout.addWidget(self.removeApptButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.appointmentList = QtWidgets.QListWidget(ViewAppointments)
        self.appointmentList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.appointmentList.setObjectName("appointmentList")
        self.verticalLayout_2.addWidget(self.appointmentList)

        self.retranslateUi(ViewAppointments)
        QtCore.QMetaObject.connectSlotsByName(ViewAppointments)

    def retranslateUi(self, ViewAppointments):
        _translate = QtCore.QCoreApplication.translate
        ViewAppointments.setWindowTitle(_translate("ViewAppointments", "ViewAppointments"))
        self.removeApptButton.setText(_translate("ViewAppointments", "Remove"))

