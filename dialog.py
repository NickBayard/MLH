# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConfirmDialog(object):
    def setupUi(self, ConfirmDialog):
        ConfirmDialog.setObjectName("ConfirmDialog")
        ConfirmDialog.resize(400, 116)
        ConfirmDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfirmDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.appointmentLabel = QtWidgets.QLabel(ConfirmDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appointmentLabel.sizePolicy().hasHeightForWidth())
        self.appointmentLabel.setSizePolicy(sizePolicy)
        self.appointmentLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.appointmentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.appointmentLabel.setObjectName("appointmentLabel")
        self.verticalLayout_2.addWidget(self.appointmentLabel)
        self.appointmentLabel2 = QtWidgets.QLabel(ConfirmDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appointmentLabel2.sizePolicy().hasHeightForWidth())
        self.appointmentLabel2.setSizePolicy(sizePolicy)
        self.appointmentLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.appointmentLabel2.setObjectName("appointmentLabel2")
        self.verticalLayout_2.addWidget(self.appointmentLabel2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfirmDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConfirmDialog)
        self.buttonBox.accepted.connect(ConfirmDialog.accept)
        self.buttonBox.rejected.connect(ConfirmDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfirmDialog)

    def retranslateUi(self, ConfirmDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfirmDialog.setWindowTitle(_translate("ConfirmDialog", "Dialog"))
        self.appointmentLabel.setText(_translate("ConfirmDialog", "TextLabel"))
        self.appointmentLabel2.setText(_translate("ConfirmDialog", "TextLabel"))

