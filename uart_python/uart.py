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



#read all the data which are input
def read_trame(trame):
    while len(trame)!=0:
     #recupération du byte de référnece   
        reference = ord(trame[0])
        adresse = reference >> 3
        data_type = reference & 3
        signe = (reference >>2) & 1
    
    #fin
        print(adresse, data_type, signe)        #debug
        if(data_type==0):                     #send a char 
            print("data type char")
            decode.read_char(trame[:3],adresse,signe)
            del trame[:3]                   #delete this part of the lsit
            
        elif(data_type==2):                   #send an int
            decode.read_int(trame[:6],adresse,signe)
            del trame[:6]   
        else: 
            print("error of type on the trame")
            save_table.append(trame)
            return

#function to read all input of a port while we haven't recieve the end
def reception():
    ser = serial.Serial('/dev/ttyUSB0')
    res=[]
    i=0
    while (fin(res)):
        i+=1
        res.append(ser.read())
    read_trame(res[:])
    ser.close()
#------------------------------------------------------------------------------
#   function de détection de caractère de fin de transmission
#------------------------------------------------------------------------------
def fin(data):
    if len(data)<3:
        return True
    elif (sum(decode.char_to_byte(data[-3:]))!=311 or data[-1]!= b'd'):
        return True
    else:
        del data[-3:]
        return False

def send_data(data):
    ser = serial.Serial('/dev/ttyUSB1')
    for i in range(len(data)):
        ser.write(bytes([data[i]]))
        print(bytes([data[i]]))
    ser.close
#------------------------------------------------------------------------------
#   debut du programme principal
#   
#------------------------------------------------------------------------------
liste=[]
liste1=[]
liste2=[]
decode.send_sht(11,9,liste)
decode.send_int(11,1,liste1)
decode.send_flt(11,12,liste2)

ser = serial.Serial('/dev/ttyUSB1')

