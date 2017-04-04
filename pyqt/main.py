#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import pyqtgraph as pyqt

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
        self.ui.graph = pyqt.PlotWidget(self.ui.frame_recie)
        #----------------- set the pyqtgraph
        self.ui.graph.setObjectName("graph")
        self.ui.horizontalLayout_5.addWidget(self.ui.graph)
        self.ui.graph.showGrid(0.1)
        self.ui.graph.enableAutoRange()
        self.ui.graph.showButtons()
        
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
        print("start to read uart") #debug
        data=[]
        decode.clear()
        #envoi de cmd de distance et orientation : amener à disparaitre
        decode.send_sht(self.ui.spinBox_x.value(),7,data)#correspond a la commande en distance
        uart.send_data(data,uart.port)
        decode.send_sht(self.ui.spinBox_y.value(),8,data)#correspond a la commande en orientation
        uart.send_data(data,uart.port)
        
        self.lecture = uart.read_uart(uart.port)
        #decla d'un timer en parrallele pour le rafraichissement de l'affichage ça marche au poil
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gr)

        self.ui.graph.clear()
        decode.send_char(1,1,data)
        uart.send_data(data,uart.port)
                                        #START  the thread
        self.lecture.start()
        self.timer.start(100)
        
        self.ui.stop_Button.clicked.connect(lambda: self.stop_read(self.lecture,self.timer))
        
    #==========================================================================
    # function to plot data from uart using QThread
    #==========================================================================         
    def update_gr(self):
        #print("ça passe")                                    #debug
        #print("timer")
        uart.mutex.lock()                       #mutex to keep your hand on data
        distance = decode.distance
        temps = np.arange(0,len(distance)*decode.pdt,decode.pdt)
        uart.mutex.unlock()
        #print(len(temps),len(distance),temps)                      #debug
        self.ui.graph.plot(temps, distance)     #plot the data   

    #==========================================================================
    # function to stop to reading and stop the plottin
    #==========================================================================   
    def stop_read(self,thr_r,thr_af):
        #print("ça rentre",thr_r) #debug
        data=[]
        decode.send_char(0,1,data)
        uart.send_data(data,uart.port)
        thr_af.stop()
        #print("reading thread is running: ",thr_r.isRunning()) #debug
        thr_r.terminate()
        thr_r.wait()
        #print("reading thread is running: ",thr_r.isRunning()) #debug        

    #==========================================================================       
    #connection at uart
    #==========================================================================
    def uart_connection(self):
        if(uart.port.isOpen()==False):
            uart.port = uart.init_uart(self.ui.lineEdit_portcom.text(),self.ui.lineEdit_baud_rate.text())
            if uart.port != 0:
                self.ui.connect_pushButton.setStyleSheet("QPushButton {background: green}")
                self.ui.connect_pushButton.setText("connected")
            else:
                self.ui.connect_pushButton.setStyleSheet("QPushButton {background: red}")
                uart.port = uart.serial.Serial()        # reinit la var uart
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