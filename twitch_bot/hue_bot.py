# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './hue-bot.ui'
#
# Created: Sun Dec 20 12:45:21 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(404, 395)
        self.central_widget = QtGui.QWidget(main_window)
        self.central_widget.setObjectName(_fromUtf8("central_widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.text_list = QtGui.QListWidget(self.central_widget)
        self.text_list.setObjectName(_fromUtf8("text_list"))
        self.verticalLayout.addWidget(self.text_list)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.config_button = QtGui.QPushButton(self.central_widget)
        self.config_button.setObjectName(_fromUtf8("config_button"))
        self.verticalLayout.addWidget(self.config_button)
        self.start_button = QtGui.QPushButton(self.central_widget)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.verticalLayout.addWidget(self.start_button)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "Hue Bot", None))
        self.config_button.setText(_translate("main_window", "Configure", None))
        self.start_button.setText(_translate("main_window", "Start Bot", None))

