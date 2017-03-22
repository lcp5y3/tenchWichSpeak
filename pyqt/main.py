#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import*
from PyQt4.QtGui import*
from interface_test import Ui_mainWind

import CRUBS_ll_decode as decode
import uart as uart

class robot_reg_app(QGroupBox):
    
    def __init__(self, parent=None):
        super (robot_reg_app, self).__init__(parent)
        self.createWidgets()
    #==========================================================================
    #slot connection-----------------------------------------------------------
    #==========================================================================
        self.ui.exit_button.clicked.connect(self.close)#--- a changer pour s'assurer fermeture de thread
        self.ui.send_pid_Button.clicked.connect(self.send_pid)
        self.ui.start_Button.clicked.connect(self.read_data)
        self.ui.connect_pushButton.clicked.connect(self.uart_connection)

    def createWidgets(self):
        self.ui = Ui_mainWind()
        self.ui.setupUi(self)
    #==========================================================================
     #function to send pid
    #==========================================================================
    def send_pid(self):
        if(self.ui.angle_checkBox.isChecked()):
            adr = 4
        else:
            adr = 1
            #envoi des données
        data = []    
        decode.send_flt(self.ui.doubleSpinBox_P.value(),adr,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_I.value(),adr+1,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_D.value(),adr+2,data)
        uart.send_data(data,uart.port)
    #==========================================================================
    # function to read data from uart using QThread
    #==========================================================================
    def read_data(self):
        data=[]
        decode.clear()
        uart.stop_reading = 0
        decode.send_sht(self.ui.spinBox_x.value(),7,data)#correspond a la commande en distance
        uart.send_data(data,uart.port)
        decode.send_sht(self.ui.spinBox_y.value(),8,data)#correspond a la commande en orientation
        uart.send_data(data,uart.port)
        self.lecture = uart.read_uart(uart.port)
        self.connect(self.ui.stop_Button,SIGNAL("clicked()"),self.lecture.stop)
        decode.send_char(1,1,data)
        uart.send_data(data,uart.port)
        self.lecture.start()
        self.ui.graph.clear()
        decode.base_temps(len(decode.distance))
        self.ui.graph.plot(decode.temps[:len(decode.distance)], decode.distance)  
    #==========================================================================
    # function to plot data from uart using QThread
    #==========================================================================
    def stop_read(self,thr):
        aaa
        
 #connection at uart
    def uart_connection(self):
        if(uart.port.isOpen()==False):
            uart.port = uart.init_uart(self.ui.lineEdit_portcom.text(),self.ui.lineEdit_baud_rate.text())
            if uart.port != 0:
                self.ui.connect_pushButton.setStyleSheet("QPushButton {background: green}")
                self.ui.connect_pushButton.setText("connected")
            else:
                self.ui.connect_pushButton.setStyleSheet("QPushButton {background: red}")
        else:
            uart.port.close()
            uart.port.__exit__
            self.ui.connect_pushButton.setStyleSheet("QPushButton {background: red}")
            self.ui.connect_pushButton.setText("unconnected")
            
#==============================================================================
if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = robot_reg_app()
	myapp.show()
	sys.exit(app.exec())

def affichage(fenetre,thread_lecture,dist):
    decode.clear()
    fenetre.graph.clear()
    while(thread_lecture.is_alive()):
        uart.mutex.acquire()
        try:
            fenetre.graph.plot(decode.temps[:len(dist)], dist)  
        except: 
            print("error affichage")
        finally:
            uart.mutex.release()
            time.sleep(0.1) 