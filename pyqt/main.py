#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import pyqtgraph as pyqt

from interface import Ui_mainWind

import CRUBS_ll_decode as decode
import uart as uart

mutex_uart = QMutex()   #protec ecriture sur uart
            
class robot_reg_app(QGroupBox):
    
    def __init__(self, parent=None):
        super (robot_reg_app, self).__init__(parent)
        self.createWidgets()
        self.init_graph()
        self.init_widget()
    #==========================================================================
    #slot connection-----------------------------------------------------------
    #==========================================================================
        self.ui.exit_button.clicked.connect(self.stop)
        self.ui.send_pid_cap_Button.clicked.connect(self.send_pid_cap)
        self.ui.send_pid_d_Button.clicked.connect(self.send_pid_d)
        self.ui.start_Button.clicked.connect(self.read_data)
        self.ui.connect_pushButton.clicked.connect(self.uart_connection)
        self.ui.stop_Button.clicked.connect(self.stop_read)
        self.ui.send_pos.clicked.connect(self.send_pos)
    #==========================================================================
    #init variable-----------------------------------------------------------
    #==========================================================================       
        self.first = True
        self.nb_clique = 0
    #==========================================================================
    #decla des threads-----------------------------------------------------------
    #==========================================================================   
    #-----timer de rafraichissement des data        
        self.refresh_var = QTimer()
        self.refresh_var.timeout.connect(self.update_disp)
    #-----timer rafraichissement du graph
        self.timer = QTimer()
    #-----thread de la lecture d'uart
        self.lecture = QThread()    #uart.read_uart(uart.port)
        
    def stop(self):
        # function to close the app.
        if(self.first==False):            
            self.stop_read()
        if(uart.port.isOpen()==True):
            self.refresh_var.stop()
        print("close the door")
        self.close()
        
        
    def init_graph(self):
        #----------------- set the pyqtgraph
        self.ui.graph = pyqt.PlotWidget(self.ui.frame_recie)
        self.ui.graph.setObjectName("graph")
        self.ui.horizontalLayout_5.addWidget(self.ui.graph)
        self.ui.graph.showGrid(0.1)
        self.ui.graph.enableAutoRange()
        self.ui.graph.showButtons()
        
    def init_widget(self):
        nb_decimal = 3
        max_dist = 1000
         #-------double spin box
        self.ui.doubleSpinBox_P_d.setDecimals(nb_decimal)
        self.ui.doubleSpinBox_I_d.setDecimals(nb_decimal)
        self.ui.doubleSpinBox_D_d.setDecimals(nb_decimal)
         
        self.ui.doubleSpinBox_P_cap.setDecimals(nb_decimal)
        self.ui.doubleSpinBox_I_cap.setDecimals(nb_decimal)
        self.ui.doubleSpinBox_D_cap.setDecimals(nb_decimal)
         #-------spin box
        self.ui.spinBox_x.setMaximum(max_dist)
        self.ui.spinBox_x.setMinimum(-max_dist)
        self.ui.spinBox_y.setMaximum(max_dist)
        self.ui.spinBox_y.setMinimum(-max_dist)
        
    def createWidgets(self):
        self.ui = Ui_mainWind()
        self.ui.setupUi(self)
    #==========================================================================
     #functions to send pid
    #==========================================================================
    def send_pid_d(self):
        print("DEBUG: send pid distance")    #debug
        adr = 1
        #envoi des données
        data = []
        mutex_uart.lock() #chope la main
        decode.send_flt(self.ui.doubleSpinBox_P_d.value(),adr,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_I_d.value(),adr+1,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_D_d.value(),adr+2,data)
        uart.send_data(data,uart.port)
        mutex_uart.unlock() #on la rend
    
    def send_pid_cap(self):
        print("DEBUG: send pid cap")    #debug
        adr = 7
                #envoi des données
        data = []   
        mutex_uart.lock() #chope la main
        decode.send_flt(self.ui.doubleSpinBox_P_cap.value(),adr,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_I_cap.value(),adr+1,data)
        uart.send_data(data,uart.port)
        decode.send_flt(self.ui.doubleSpinBox_D_cap.value(),adr+2,data)
        uart.send_data(data,uart.port)
        mutex_uart.unlock() #on la rend
        
    #==========================================================================
     #functions to send pid
    #==========================================================================
    
    def send_pos(self):
        print("DEBUG: send pid cap")    #debug
        adr = 3
                #envoi des données
        data = []   
        mutex_uart.lock() #chope la main
        decode.send_int(self.ui.spinBox_x.value(),adr,data)
        uart.send_data(data,uart.port)
        decode.send_int(self.ui.spinBox_y.value(),adr+1,data)
        uart.send_data(data,uart.port)
    #==========================================================================
    # function to read data from uart using QThread
    #==========================================================================
    def read_data(self):
        if(self.nb_clique==0):# assure la mono commande des threads 
           self.nb_clique=1
            #print("start to read uart") #debug
           data=[]
           decode.clear()
           #envoi de cmd de distance et orientation : amener à disparaitre
           decode.send_int(self.ui.spinBox_x.value(),3,data)#correspond a la commande en distance
           uart.send_data(data,uart.port)
           #print("la data que j'envoi est la : ",data)    #debug
           decode.send_int(self.ui.spinBox_y.value(),4,data)#correspond a la commande en orientation
           uart.send_data(data,uart.port)
           
           if(self.first==True):
               self.lecture = uart.read_uart(uart.port)
               #decla d'un timer en parrallele pour le rafraichissement de l'affichage ça marche au poil
               self.timer.timeout.connect(self.update_gr)
               self.first = False
               print("crea des thread")    #debug
               
           self.ui.graph.clear()
           decode.send_char(1,1,data)
           #print("la data que j'envoi est la : ",data)    #debug
           mutex_uart.lock()
           uart.send_data(data,uart.port)
           uart.send_data(data,uart.port)
           uart.send_data(data,uart.port)
           mutex_uart.unlock() #on la rend
                                            #START  the thread
           self.lecture.start()
           self.timer.start(100)
           
   #-------decla d'un timer pour rafraichir la valeurs des variables regulièrement------
           print("DEBUG: on lance le timer de rafraich")   #debug
        
        
    #==========================================================================
    # function to plot data from uart using QThread
    #==========================================================================         
    def update_gr(self):
        #print("ça passe")                                    #debug
        #print("timer")
        uart.mutex.lock()                       #mutex to keep your hand on data
        distance = decode.distance
        commande = decode.theta
        #print("DEBUG: valeur de theta lu ",commande)
        temps = np.arange(0,len(distance)*decode.pdt,decode.pdt)
        temps2 = np.arange(0,len(commande)*decode.pdt,decode.pdt)
        #print(len(temps),len(distance),temps)                      #debug
        try:
            self.ui.graph.plot(temps, distance,pen='r')     #plot the data 
            self.ui.graph.plot(temps2,commande,pen='b')
        except:
            print("DEBUG: pb de dimmension tab graph")
        uart.mutex.unlock()
        self.nb_clique=0

    #==========================================================================
    # function to stop to reading and stop the plottin
    #==========================================================================   
    def stop_read(self):#self,thr_r,thr_af):
        data=[]
        decode.send_char(0,1,data)
        #envoi plusieurs fois la commande d'arret afin d'être sur de la lecture
        mutex_uart.lock() #on prend la main
        uart.send_data(data,uart.port)
        uart.send_data(data,uart.port)
        uart.send_data(data,uart.port)
        mutex_uart.unlock() #on la rend
        self.timer.stop()
        self.refresh_var.stop()
        #print("reading thread is running: ",thr_r.isRunning()) #debug
        self.lecture.terminate()
        self.lecture.wait()
        print("stop reading") #debug
        #print("reading thread is running: ",thr_r.isRunning()) #debug        


    #==========================================================================       
    #update display of pid data 
    #==========================================================================
    def update_disp(self):
        value=[]
        print("DEBUG: rafraichissement qui veut un rafraichissement!")  #debug
        #------- on envoie les demandes de valeurs
        mutex_uart.lock() #on la prend
        decode.send_flt(0,4,value)
        uart.send_data(value,uart.port)
        decode.send_flt(0,5,value)
        uart.send_data(value,uart.port)
        decode.send_flt(0,6,value)
        uart.send_data(value,uart.port)
        decode.send_flt(0,10,value)
        uart.send_data(value,uart.port)
        decode.send_flt(0,11,value)
        uart.send_data(value,uart.port)
        decode.send_flt(0,12,value)
        uart.send_data(value,uart.port)
        mutex_uart.unlock() #on la rend
        #----display value of pid
        self.ui.label_pv.setText(str(decode.flt_table[4]))
        self.ui.label_iv.setText(str(decode.flt_table[5]))
        self.ui.label_dv.setText(str(decode.flt_table[6]))
        print("DEBUG : valeur pid cap",decode.flt_table[10])    #debug
        
        self.ui.label_p_cap.setText(str(decode.flt_table[10]))
        self.ui.label_i_cap.setText(str(decode.flt_table[11]))
        self.ui.label_d_cap.setText(str(decode.flt_table[12]))

    #==========================================================================       
    #connection at uart
    #==========================================================================
    def uart_connection(self):
        if(uart.port.isOpen()==False):
            uart.port = uart.init_uart(self.ui.lineEdit_portcom.text(),self.ui.lineEdit_baud_rate.text())
            if uart.port != 0:
                self.ui.connect_pushButton.setStyleSheet("QPushButton {background: green}")
                self.ui.connect_pushButton.setText("connected")
           
                #self.refresh_var.start(2500)
                #print("DEBUG: timer lancée")    #debug 

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
