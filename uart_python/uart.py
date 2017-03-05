# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#bibliotheque import are here
import serial
import CRUBS_ll_decode as decode

save_table=[]
#function are here
def read_trame(port):
    trame=[]
    while(!check_end()):#code du check à faire chef
        if(port.inWaiting):
            trame.append(port.read())
            if(trame[-1]==stop_b):
                #mettre ici la lecture


#read all the data which are input--------------------------------------------
def read_trame_type(trame):
    while len(trame)!=0:
     #recupération du byte de référnece   
        reference = ord(trame[1])
        adresse = reference >> 3
        data_type = reference & 3
        signe = (reference >>2) & 1
    #fin
        print(adresse, data_type, signe)        #debug
        if(data_type==0):                     #send a char 
            print("data type char")
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
    ser = serial.Serial(port)
    ser.baudrate = bdrate
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
decode.send_sht(32000,7,dist)

ser = serial.Serial('/dev/ttyUSB0')

