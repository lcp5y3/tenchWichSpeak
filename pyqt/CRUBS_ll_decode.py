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
cmd_d=[]
cmd_a=[]
theta=[]
#--------------------------float----------------------------------------------
p_dist=0
i_dist=0
d_dist=0

p_ang=0
i_ang=0
d_ang=0
#------------var de sauvegarde de data -------------------------------------
char_table=[0,1,2,3,4,5,6]
int_table=[0,1,2,distance,angle,cmd_d]
short_table=[0,1,2,3,4,5,cmd_a]
flt_table=[0,1,2,3,p_dist,i_dist,d_dist,7,8,9,p_ang,i_ang,d_ang,theta]

#----------------var de paramètrage------------------------------------------
pdt = 0.01      #pas de temps pour l'affichage du temps
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
seuil_max = 1000000000

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
    #return variable-1-pow(2,nb_bit)
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
        cmd_d[:]=[]
        theta[:]=[]
#-----------------------------------------------------------------------------
#reading functions
#-----------------------------------------------------------------------------
    
#read ca char with the protocole CRUBS_ll-------------------------------------
def read_char(trame,adresse,signe): # reste le signe a regardr ici
        char_table[adresse].append(trame[1])

#read an short with the protocole CRUBS_ll-------------------------------------
def read_sht(trame,adresse,signe):
        resultat =0
        for i in range(len(trame)):
                resultat = resultat <<8
                resultat += trame[i]
        #print("DEBUG: short signe ",signe," resultat: ",resultat)
        if(signe == 0):
            short_table[adresse].append(resultat)
        else:
            short_table[adresse].append(complementA2(resultat, b_short))
    
        #print("DEBUG:  valeur ",short_table[adresse][-1],"|| adresse: ",adresse)
#read an int with the protocole CRUBS_ll--------------------------------------
def read_int(trame,adresse,signe):
        resultat = 0
        for i in range(len(trame)):
            resultat = resultat <<8
            resultat += trame[i]   
        if(signe == 0):
            int_table[adresse].append(resultat)
        else:
            int_table[adresse].append(complementA2(resultat, b_int))
            
#read an int with the protocole CRUBS_ll--------------------------------------
def read_flt(data,adresse,signe):
        resultat = 0
        #print("DEBUG: valeur de la trame dans le read flt ",data)
        for i in range(len(data)):
            resultat = resultat <<8
            resultat += data[i]
        #print("DEBUG: float resultat ", resultat)
        if(signe == 0):
            flt_table[adresse].append(resultat/flt_coef)
        else:
            flt_table[adresse].append(complementA2(resultat, b_flt)/flt_coef)
        #print("DEBUG:  valeur ",flt_table[adresse][-1],"|| adresse: ",adresse)

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
        data = complementA2(data,b_char)
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
        data = complementA2(data,b_short)
        print(hex(data))                  #debug
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
        data = complementA2(data,b_int)
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
        data = complementA2(data,b_flt)
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


