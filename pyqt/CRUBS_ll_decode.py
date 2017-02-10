# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:23:50 2017

@author: lcp5y3
"""

#----------------------------------------------------------------------------
#   file of function which allow to decode data from uart protocole 
#   CRUBS_ll
#-----------------------------------------------------------------------------
#define and other prerocessing are here
char_table=[]
int_table=[]
short_table=[]
save_table=[]

b_int = 32
b_char = 8
b_short = 16
size_int = 6
size_char = 3
size_short = 4
#-----------------------------------------------------------------------------
# function two's complement
#-----------------------------------------------------------------------------
def complementA2(variable, nb_bit):
    return -1*((variable-1)^(pow(2,nb_bit)-1))          # var-1 xor 2puissanceX -1
    
#transforme char en byte read like int
def char_to_byte(trame):
    for i in range(len(trame)):
        trame[i]=ord(trame[i])
    return trame
    
#-----------------------------------------------------------------------------
#reading functions
#-----------------------------------------------------------------------------

#read ca char with the protocole CRUBS_ll
def read_char(data,adresse,signe):
    trame = char_to_byte(data)
    checksum = sum(trame[:size_char-1])
    if((checksum&0x000000ff)!=data[size_char]):
        print("error of checksum")
        exit
    else:
        char_table.append(data[1])

#read an short with the protocole CRUBS_ll
def read_short(data,adresse,signe):
    trame = char_to_byte(data)
    checksum = sum(trame[:3])
    print(trame, (checksum & 0x000000ff))
    if((checksum & 0x000000ff)!=data[3]):
        print("error of checksum")
        exit
    else:
        del trame[-1]
        del trame[0]
        resultat =0
        for i in range(len(trame)):
                resultat += trame[i]
                resultat = resultat <<8
        if(signe == 0):
            short_table.append(resultat)
        else:
            short_table.append(complementA2(resultat, size_short))
            
#read an int with the protocole CRUBS_ll
def read_int(data,adresse,signe):
    trame = char_to_byte(data)
    checksum = sum(trame[:5])
    if((checksum & 0x000000ff)!=data[5]):
        print("error of checksum")
        exit
    else:
        del trame[0]
        del trame[-1]
        resultat = trame[0]
        print(resultat)
        del trame[0]
        for i in range(len(trame)):
            resultat = resultat <<8
            resultat += trame[i]
        print(resultat)
        if(signe == 0):
            int_table.append(resultat)
        else:
            int_table.append(complementA2(resultat, b_int))

#-----------------------------------------------------------------------------
#     sending function
#-----------------------------------------------------------------------------
def send_pid(coef_p, coef_i, coef_d):
    print("c'est ok ", coef_p)