# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_test.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import CRUBS_ll_decode as decode


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

class Ui_mainWind(object):
    def setupUi(self, mainWind):
#fenetre principale
        mainWind.setObjectName(_fromUtf8("mainWind"))
        mainWind.resize(700, 450)
#exit button
        self.exit_button = QtGui.QPushButton(mainWind)
        self.exit_button.setGeometry(QtCore.QRect(610, 420, 83, 24))
        self.exit_button.setObjectName(_fromUtf8("exit_button"))
#save button
        self.save_button = QtGui.QPushButton(mainWind)
        self.save_button.setGeometry(QtCore.QRect(530, 420, 83, 24))
        self.save_button.setObjectName(_fromUtf8("save_button"))
#pid frame button label
        self.reg_pid_frame = QtGui.QFrame(mainWind)
        self.reg_pid_frame.setGeometry(QtCore.QRect(10, 20, 221, 91))
        self.reg_pid_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.reg_pid_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.reg_pid_frame.setObjectName(_fromUtf8("reg_pid_frame"))
        self.label_P = QtGui.QLabel(self.reg_pid_frame)
        self.label_P.setGeometry(QtCore.QRect(10, 40, 57, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_P.setFont(font)
        self.label_P.setTextFormat(QtCore.Qt.AutoText)
        self.label_P.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_P.setObjectName(_fromUtf8("label_P"))
        self.doubleSpinBox_P = QtGui.QDoubleSpinBox(self.reg_pid_frame)
        self.doubleSpinBox_P.setGeometry(QtCore.QRect(10, 60, 62, 22))
        self.doubleSpinBox_P.setObjectName(_fromUtf8("doubleSpinBox_P"))
    
        self.doubleSpinBox_I = QtGui.QDoubleSpinBox(self.reg_pid_frame)
        self.doubleSpinBox_I.setGeometry(QtCore.QRect(80, 60, 62, 22))
        self.doubleSpinBox_I.setObjectName(_fromUtf8("doubleSpinBox_I"))
        
        self.doubleSpinBox_D = QtGui.QDoubleSpinBox(self.reg_pid_frame)
        self.doubleSpinBox_D.setGeometry(QtCore.QRect(150, 60, 62, 22))
        self.doubleSpinBox_D.setObjectName(_fromUtf8("doubleSpinBox_D"))
        
        self.label_I = QtGui.QLabel(self.reg_pid_frame)
        self.label_I.setGeometry(QtCore.QRect(80, 40, 57, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_I.setFont(font)
        self.label_I.setTextFormat(QtCore.Qt.AutoText)
        self.label_I.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_I.setObjectName(_fromUtf8("label_I"))
        self.label_D = QtGui.QLabel(self.reg_pid_frame)
        self.label_D.setGeometry(QtCore.QRect(150, 40, 57, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_D.setFont(font)
        self.label_D.setTextFormat(QtCore.Qt.AutoText)
        self.label_D.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_D.setObjectName(_fromUtf8("label_D"))
        self.label_title_pid = QtGui.QLabel(self.reg_pid_frame)
        self.label_title_pid.setGeometry(QtCore.QRect(10, 10, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_title_pid.setFont(font)
        self.label_title_pid.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title_pid.setObjectName(_fromUtf8("label_title_pid"))
        self.send_pid_Button = QtGui.QPushButton(self.reg_pid_frame)
        self.send_pid_Button.setGeometry(QtCore.QRect(170, 10, 41, 24))
        self.send_pid_Button.setObjectName(_fromUtf8("send_pid_Button"))
        self.frame = QtGui.QFrame(mainWind)
        self.frame.setGeometry(QtCore.QRect(230, 20, 461, 91))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))

        self.retranslateUi(mainWind)
        QtCore.QObject.connect(self.exit_button, QtCore.SIGNAL(("clicked()")), mainWind.close)
        QtCore.QObject.connect(self.send_pid_Button, QtCore.SIGNAL("clicked()"), self.slot_send_pid)        
        QtCore.QMetaObject.connectSlotsByName(mainWind)

    def retranslateUi(self, mainWind):
        mainWind.setWindowTitle(_translate("mainWind", "GroupBox", None))
        mainWind.setTitle(_translate("mainWind", "GroupBox", None))
        self.exit_button.setText(_translate("mainWind", "exit", None))
        self.save_button.setText(_translate("mainWind", "save", None))
        self.label_P.setText(_translate("mainWind", "P", None))
        self.label_I.setText(_translate("mainWind", "I", None))
        self.label_D.setText(_translate("mainWind", "D", None))
        self.label_title_pid.setText(_translate("mainWind", "réglage du PID", None))
        self.send_pid_Button.setText(_translate("mainWind", "send", None))

    def slot_send_pid(self):
        decode.send_pid(self.doubleSpinBox_P.value(),self.doubleSpinBox_I.value(),self.doubleSpinBox_D.value())
        
    def slot_send_data(self):
        print("hello")