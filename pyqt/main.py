#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import*
from PyQt4.QtGui import*
from interface_test import Ui_mainWind

class robot_reg_app(QGroupBox):
	def __init__(self, parent=None):
		super (robot_reg_app, self).__init__(parent)
		self.createWidgets()

	def createWidgets(self):
		self.ui = Ui_mainWind()
		self.ui.setupUi(self)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = robot_reg_app()
	myapp.show()
	sys.exit(app.exec())

