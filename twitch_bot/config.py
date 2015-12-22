# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './config.ui'
#
# Created: Mon Dec 21 23:21:10 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(442, 414)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 11, 1, 1, 1)
        self.admin_textbox = QtGui.QLineEdit(Dialog)
        self.admin_textbox.setObjectName(_fromUtf8("admin_textbox"))
        self.gridLayout.addWidget(self.admin_textbox, 6, 3, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 12, 1, 1, 1)
        self.color_end_textbox = QtGui.QLineEdit(Dialog)
        self.color_end_textbox.setObjectName(_fromUtf8("color_end_textbox"))
        self.gridLayout.addWidget(self.color_end_textbox, 14, 3, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 1, 1, 1)
        self.button_box = QtGui.QDialogButtonBox(Dialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.Save)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.gridLayout.addWidget(self.button_box, 15, 3, 1, 1)
        self.channel_textbox = QtGui.QLineEdit(Dialog)
        self.channel_textbox.setObjectName(_fromUtf8("channel_textbox"))
        self.gridLayout.addWidget(self.channel_textbox, 1, 3, 1, 1)
        self.hueBridgeIPLabel = QtGui.QLabel(Dialog)
        self.hueBridgeIPLabel.setObjectName(_fromUtf8("hueBridgeIPLabel"))
        self.gridLayout.addWidget(self.hueBridgeIPLabel, 9, 1, 1, 1)
        self.hueGroupNameLabel = QtGui.QLabel(Dialog)
        self.hueGroupNameLabel.setObjectName(_fromUtf8("hueGroupNameLabel"))
        self.gridLayout.addWidget(self.hueGroupNameLabel, 10, 1, 1, 1)
        self.twitchUsernameLabel = QtGui.QLabel(Dialog)
        self.twitchUsernameLabel.setObjectName(_fromUtf8("twitchUsernameLabel"))
        self.gridLayout.addWidget(self.twitchUsernameLabel, 0, 1, 1, 1)
        self.username_textbox = QtGui.QLineEdit(Dialog)
        self.username_textbox.setObjectName(_fromUtf8("username_textbox"))
        self.gridLayout.addWidget(self.username_textbox, 0, 3, 1, 1)
        self.twitchChannelLabel = QtGui.QLabel(Dialog)
        self.twitchChannelLabel.setObjectName(_fromUtf8("twitchChannelLabel"))
        self.gridLayout.addWidget(self.twitchChannelLabel, 1, 1, 1, 1)
        self.oauth_textbox = QtGui.QLineEdit(Dialog)
        self.oauth_textbox.setObjectName(_fromUtf8("oauth_textbox"))
        self.gridLayout.addWidget(self.oauth_textbox, 4, 3, 1, 1)
        self.hue_group_textbox = QtGui.QLineEdit(Dialog)
        self.hue_group_textbox.setObjectName(_fromUtf8("hue_group_textbox"))
        self.gridLayout.addWidget(self.hue_group_textbox, 10, 3, 1, 1)
        self.oAuthTokenLabel = QtGui.QLabel(Dialog)
        self.oAuthTokenLabel.setObjectName(_fromUtf8("oAuthTokenLabel"))
        self.gridLayout.addWidget(self.oAuthTokenLabel, 4, 1, 1, 1)
        self.hue_ip_textbox = QtGui.QLineEdit(Dialog)
        self.hue_ip_textbox.setObjectName(_fromUtf8("hue_ip_textbox"))
        self.gridLayout.addWidget(self.hue_ip_textbox, 9, 3, 1, 1)
        self.color_start_textbox = QtGui.QLineEdit(Dialog)
        self.color_start_textbox.setObjectName(_fromUtf8("color_start_textbox"))
        self.gridLayout.addWidget(self.color_start_textbox, 13, 3, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 13, 1, 1, 1)
        self.flash_count_spinner = QtGui.QSpinBox(Dialog)
        self.flash_count_spinner.setMinimum(1)
        self.flash_count_spinner.setMaximum(10)
        self.flash_count_spinner.setProperty("value", 3)
        self.flash_count_spinner.setObjectName(_fromUtf8("flash_count_spinner"))
        self.gridLayout.addWidget(self.flash_count_spinner, 12, 3, 1, 1)
        self.flash_speed_slider = QtGui.QSlider(Dialog)
        self.flash_speed_slider.setMinimum(1)
        self.flash_speed_slider.setMaximum(10)
        self.flash_speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.flash_speed_slider.setObjectName(_fromUtf8("flash_speed_slider"))
        self.gridLayout.addWidget(self.flash_speed_slider, 11, 3, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 14, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.username_textbox, self.channel_textbox)
        Dialog.setTabOrder(self.channel_textbox, self.oauth_textbox)
        Dialog.setTabOrder(self.oauth_textbox, self.admin_textbox)
        Dialog.setTabOrder(self.admin_textbox, self.hue_ip_textbox)
        Dialog.setTabOrder(self.hue_ip_textbox, self.hue_group_textbox)
        Dialog.setTabOrder(self.hue_group_textbox, self.flash_speed_slider)
        Dialog.setTabOrder(self.flash_speed_slider, self.flash_count_spinner)
        Dialog.setTabOrder(self.flash_count_spinner, self.color_start_textbox)
        Dialog.setTabOrder(self.color_start_textbox, self.color_end_textbox)
        Dialog.setTabOrder(self.color_end_textbox, self.button_box)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "Flash Speed", None))
        self.label_5.setText(_translate("Dialog", "Flash Count", None))
        self.color_end_textbox.setText(_translate("Dialog", "65535", None))
        self.label_6.setText(_translate("Dialog", "Admin Username", None))
        self.hueBridgeIPLabel.setText(_translate("Dialog", "Hue Bridge IP", None))
        self.hueGroupNameLabel.setText(_translate("Dialog", "Hue Group Name", None))
        self.twitchUsernameLabel.setText(_translate("Dialog", "Twitch Username", None))
        self.twitchChannelLabel.setText(_translate("Dialog", "Twitch Channel", None))
        self.oAuthTokenLabel.setText(_translate("Dialog", "OAuth Token", None))
        self.color_start_textbox.setText(_translate("Dialog", "46920", None))
        self.label_3.setText(_translate("Dialog", "Flash Color Start", None))
        self.label_4.setText(_translate("Dialog", "Flash Color End", None))

