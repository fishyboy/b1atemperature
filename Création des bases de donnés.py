# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:13:25 2017

@author: Guillaume Touzé
"""

#/!\ ne pas relancer ce code, la base est déjà créée

import csv
import sqlite3


#Création de la base de donnés pour les stations et la température        
conn = sqlite3.connect('meteo.sqlite')
c = conn.cursor()
c.execute(''' CREATE TABLE station_meteo (Id int, Nom_station text, Latitude text, Longitude text, Altitude int)''')
c.execute(''' CREATE TABLE Temperature (Id_station int, Date int, T_moy int, Qualite_T_moy int, T_min int, Qualite_T_min int, T_max int, Qualite_T_max int)''')

#Création de la base de donnés pour les graphiques 
conn = sqlite3.connect('graphiques.sqlite')
c = conn.cursor()
c.execute(''' CREATE TABLE image (Id int, Id_station int, T_type text, date_debut int, date_fin int)''')
conn.close()

#Ouverture et lecture du premier fichier CSV
with open('stations-meteo.csv', newline='',encoding='utf-8') as csvfile:
    lecture=csv.reader(csvfile, delimiter=';')        
#Remplissage de la table
    i=False
    for row in lecture:
        if i==False:
            i=True
        else:
            c.execute("INSERT INTO station_meteo VALUES ("+row[0]+",'"+row[1]+"','"+row[2]+ "','"+ row[3]+"',"+ row[4]+")")

conn.commit()

#Ouverture et lecture du 2nd fichier CSV
with open('tem p-histo.csv', newline='',encoding='utf-8') as csvfile:
    lecture=csv.reader(csvfile, delimiter=';')        
#Remplissage de la table
    i=False
    for row in lecture:
        if i==False:
            i=True
        else:
            c.execute("INSERT INTO Temperature VALUES ("+row[0]+","+row[1]+","+row[2]+ ","+ row[3]+","+ row[4]+","+row[5]+","+row[6]+","+row[7]+")")

conn.commit()
conn.close()