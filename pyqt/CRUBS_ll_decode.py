# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:23:50 2017

@author: lcp5y3
"""

#----------------------------------------------------------------------------
#   file of function which allow to decode data from uart protocole 
#   CRUBS_ll
#-----------------------------------------------------------------------------

#----------------------short--------------------------------------------------
distance=[]
angle=[]
temps=[]
#--------------------------float----------------------------------------------
p_dist=0
i_dist=0
d_dist=0

p_ang=0
i_ang=0
d_ang=0
#------------var de sauvegarde de data -------------------------------------
char_table=[0,1,2,3,4,5,6]
int_table=[(),()]
short_table=[0,1,2,3,4,5,6,7,8,distance,angle]
flt_table=[0,1,2,3,p_dist,i_dist,d_dist,7,8,9,p_ang,i_ang,d_ang]

#----------------var de paramètrage------------------------------------------
b_int = 32
b_char = 8
b_short = 16
b_flt = 32

ch_mask = 0
sht_mask = 1
int_mask = 2
flt_mask = 3

byte_mask = 255
flt_coef = 1000

size_int = 6
size_char = 3
size_short = 4

start_b = 252
stop_b = 244
#-----------------------------------------------------------------------------
# function two's complement
#-----------------------------------------------------------------------------
def complementA2(variable, nb_bit):
    return -1*((variable-1)^(pow(2,nb_bit)-1))          # var-1 xor 2puissanceX -1
    
#transforme char en byte read like int
def char_to_byte(trame):
    for i in range(len(trame)):
        trame[i]=ord(trame[i])
#    return trame
    
def checksum(data):
    return(sum(data[:]) & byte_mask)

def base_temps(longueur):
    bt = 0.01
    temps[:]=[]
    for i in range(longueur):
        temps.append(bt*(1+i))

def clear():
        distance[:]=[]
        temps[:]=[]
        angle[:]=[]
#-----------------------------------------------------------------------------
#reading functions
#-----------------------------------------------------------------------------
    
#read ca char with the protocole CRUBS_ll-------------------------------------
def read_char(trame,adresse,signe):
    checksum = sum(trame[:size_char-1])
    if((checksum&0x000000ff)!=trame[size_char]):
        print("error of checksum")
        exit
    else:
        char_table[adresse].append(trame[1])

#read an short with the protocole CRUBS_ll-------------------------------------
def read_sht(trame,adresse,signe):
    checksum = sum(trame[:3])
    if((checksum & 0x000000ff)!=trame[3]):
        print("error of checksum")
        exit
    else:
        del trame[-1]
        del trame[0]
        resultat =0
        for i in range(len(trame)):
                resultat = resultat <<8
                resultat += trame[i]
                
        if(signe == 0):
            short_table[adresse].append(resultat)
        else:
            short_table[adresse].append(complementA2(resultat, size_short))
            
#read an int with the protocole CRUBS_ll--------------------------------------
def read_int(trame,adresse,signe):
    checksum = sum(trame[:5])
    if((checksum & 0x000000ff)!=trame[5]):
        print("error of checksum")
        exit
    else:
        del trame[0]
        del trame[-1]
        resultat = trame[0]
        del trame[0]
        for i in range(len(trame)):
            resultat = resultat <<8
            resultat += trame[i]
        if(signe == 0):
            int_table[adresse].append(resultat)
        else:
            int_table[adresse].append(complementA2(resultat, b_int))
            
#read an int with the protocole CRUBS_ll--------------------------------------
def read_flt(data,adresse,signe):
    checksum = sum(data[:5])
    if((checksum & 0x000000ff)!=data[5]):
        print("error of checksum")
        exit
    else:
        del data[0]
        del data[-1]
        resultat = data[0]
        del data[0]
        for i in range(len(data)):
            resultat = resultat <<8
            resultat += data[i]
        if(signe == 0):
            flt_table[adresse]=(resultat/flt_coef)
        else:
            flt_table[adresse]=(complementA2(resultat, b_flt)/flt_coef)

#function to detect the end of a trame---------------------------------------
def eot(trame):
    if(trame == stop_b):
        return True
    else: 
        return False
def eo_transmit(trame):
    if(len(trame)>=3):    
        if(sum(trame[-3:])==311 and trame[-1]==100):
            print("fin de transmission")
            return True
    else:
        return False
#-----------------------------------------------------------------------------
#     sending function
#-----------------------------------------------------------------------------
#function to add the start/stop byte
def ss_byte(data):
    data.append(stop_b)
    data.insert(0,start_b)

# function to send a char-----------------------------------------------------
def send_char(data,adresse,char_data):
    char_data[:]=[] #on nettoie
    #ajout du bit adresse signe type
    char_data.append(adresse)
    if(data<0):
        char_data[0]=(char_data[0]<<1)+1
    else:
        char_data[0]=char_data[0]<<1
    char_data[0]=(char_data[0]<<2)+ch_mask
    #envoi
    char_data.append(data)
    char_data.append(checksum(char_data[:]))
    ss_byte(char_data) #ajout start/stop byte

# function to send a short----------------------------------------------------
def send_sht(data,adresse,sht_data):
    sht_data[:]=[]
    #prepa du bit d'adresse
    sht_data.append(adresse)
    if(data<0):
        sht_data[0]=(sht_data[0]<<1)+1
        data = abs(data)
    else:
        sht_data[0] = sht_data[0]<<1
    sht_data[0]=(sht_data[0]<<2)+sht_mask
#prepa des datas
    sht_data.append(data >> 8)
    sht_data.append(data & byte_mask)
    sht_data.append(checksum(sht_data[:]))
#prepa du byte de start
    ss_byte(sht_data)

#function to send an int------------------------------------------------------
def send_int(data,adresse,int_data):
    int_data[:]=[] #on nettoie
    #ajout du bit adresse signe type
    int_data.append(adresse)
    if(data<0):
        int_data[0]=(int_data[0]<<1)+1
    else:
        int_data[0]=int_data[0]<<1
    int_data[0]=(int_data[0]<<2)+int_mask
    #envoi
    int_data.append(data >> 24)
    int_data.append((data >> 16) & byte_mask)
    int_data.append((data >> 8) & byte_mask)
    int_data.append((data & 15) & byte_mask)
    int_data.append(checksum(int_data[:]))
    ss_byte(int_data) #ajout start/stop byte

#function to send a float-----------------------------------------------------
def send_flt(data,adresse,flt_data):
    flt_data[:]=[]
        #ajout du bit adresse signe type
    flt_data.append(adresse)
    if(data<0):
        flt_data[0]=(flt_data[0]<<1)+1
    else:
        flt_data[0]=flt_data[0]<<1
    flt_data[0]=(flt_data[0]<<2)+flt_mask
    
    #adaptation des données
    data=int(data*flt_coef)
    flt_data.append(data >> 24)
    flt_data.append((data >> 16) & byte_mask)
    flt_data.append((data >> 8) & byte_mask)
    flt_data.append((data & 15) & byte_mask)
    flt_data.append(checksum(flt_data[:]))
    ss_byte(flt_data) #ajout start/stop byte
    
#debug function---------------------------------------------------------------
def print_list(liste):
    for i in range(len(liste)):
        print(bin(liste[i]))


