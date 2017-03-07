# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#bibliotheque import are here
import serial
import time
from threading import Thread
import CRUBS_ll_decode as decode

save_table=[]
#function are here
#function to read in continous mode  the uart input
class read_uart(Thread):
    
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self, port):

        Thread.__init__(self)
        self.port = port

    def run(self):

        """Code à exécuter pendant l'exécution du thread."""
        trame=[]    
        while(decode.eo_transmit(trame)!=True):
            if(self.port.inWaiting()!=0):
                trame.append(ord(self.port.read(1)))
                if(trame[-1]==decode.stop_b):
                    try:
                        print(trame)
                        read_trame_type(trame[trame.index(decode.start_b)+1:trame.index(decode.stop_b)])
                    except:
                        print("erreur lecture pas de byte de start")
                    trame[:]=[]
                    
            else:
                print("attente de données")
                time.sleep(0.1)
                
#read all the data which are input--------------------------------------------
def read_trame_type(trame):
    print("read_trame_type",trame)
    reference = trame[0]
    adresse = reference >> 3
    data_type = reference & 3
    signe = (reference >>2) & 1
#fin
    print('adr : ',adresse,'type : ', data_type,'signe : ', signe)        #debug
    if(data_type==0):                     #send a char 
        decode.read_char(trame[:3],adresse,signe)
        del trame[:3]                   #delete this part of the lsit
    elif(data_type==1):                   #send an int
        decode.read_sht(trame[:4],adresse,signe)
        del trame[:6]   
    elif(data_type==2):                   #send an int
        decode.read_int(trame[:6],adresse,signe)
        del trame[:6]   
    elif(data_type==3):                   #send an int
        decode.read_flt(trame[:6],adresse,signe)
        del trame[:6]              
    else: 
        print("error of type on the trame")
        save_table.append(trame)
        return

#function to read all input of a port while we haven't recieve the end--------
def init_uart(port,bdrate):
    try:
        ser = serial.Serial(port)
        ser.baudrate = bdrate
        print("port ouvert")
    except:
        print("error, ouverture du port impossible")
#------------------------------------------------------------------------------
#   function de détection de caractère de fin de transmission
#------------------------------------------------------------------------------
def send_data(data):
    ser = serial.Serial('/dev/ttyUSB0')
    for i in range(len(data)):
        ser.write(bytes([data[i]]))
        print(bytes([data[i]]))
    ser.close
#------------------------------------------------------------------------------
#   debut du programme principal
#   
#------------------------------------------------------------------------------
pd=[]
po=[]
dist=[]
p=8
decode.send_flt(p,1,pd)
decode.send_flt(p/2,7,po)
decode.send_sht(100,7,dist)

ser = serial.Serial('/dev/ttyUSB0')
lecture = read_uart(ser)
lecture.start()
lecture.join()