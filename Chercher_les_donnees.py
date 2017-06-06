# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 12:23:58 2017

@author: Guillaume Touzé
"""

import sqlite3
import matplotlib.pyplot as plt
#from pylab import plot.savefig

#repertoire_image="D:\ECL\S6\informatique\Projet Application Web\TD4 projet d application web\Courbes\"

#Pour avoir la température moyenne, min ou max dans la station séléctionnée à une date donnée
def T_station(Id_station,date,T_type):             #où T_type vaut moy, min ou max
    conn = sqlite3.connect('meteo.sqlite')
    c=conn.cursor()
    c.execute("SELECT * FROM Temperature WHERE Id_station="+str(Id_station)+" AND Date="+str(date))
    row = c.fetchall()
    conn.close()
    if T_type=='moy':
        return (row[0][2], row[0][3])
    if T_type=='min':
        return (row[0][4], row[0][5])
    if T_type=='max':
        return (row[0][6], row[0][7])
    else: 
        print ("Mauvais T_type indiqué")

#permet de renvoyer la liste des temps et des températures (en °C) entre deux dates pour une station donnée
def T_station_liste(Id_station, date_debut,date_fin,T_type,intervalle=True):        #où T_type vaut moy, min ou max ; mettre intervalle = False (donc mettre False) si on veut toutes ls températures depuis 40 ans
    conn = sqlite3.connect('meteo.sqlite')
    c=conn.cursor()
    
    if intervalle:
        c.execute("SELECT * FROM Temperature WHERE Id_station="+str(Id_station)+" AND Date>="+str(date_debut)+" AND Date<="+str(date_fin))
    else:
        c.execute("SELECT * FROM Temperature WHERE Id_station="+str(Id_station))
    row = c.fetchall()
    conn.close()
    L_temps=[]
    L_temperature=[]
    if T_type=='moy':
        indic=2
    if T_type=='min':
        indic=4
    if T_type=='max':
        indic=6
    for i in row:
        if i[indic+1]==0:
            L_temps.append(i[1])
            L_temperature.append(i[indic]/10)
    return (L_temps,L_temperature)
    
#/!\ il faut gérer en amont le problème des stations répertoriées mais qui n'ont pas de donnés de température(il y en a beaucoup)    
def tracer_courbe(Id_station, date_debut,date_fin,T_type):
    assert donnees_existantes(Id_station)==True
    valeurs=T_station_liste(Id_station, date_debut,date_fin,T_type)
    #temps=valeurs[0]
    temperature=valeurs[1]
    #Ajout de l'image dans la base de données
    conn = sqlite3.connect('graphiques.sqlite')
    c = conn.cursor()
    c.execute("SELECT MAX(Id) FROM image")
    maxi_id=c.fetchall()
    new_id= maxi_id[0][0]+1
    c.execute("INSERT INTO image VALUES ("+str(new_id)+","+str(Id_station)+",'"+T_type+"',"+str(date_debut)+ ","+str(date_fin)+")")
    conn.commit()
    conn.close()
    #Accès au nom de la station
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    c.execute("SELECT Nom_station FROM station_meteo WHERE Id="+str(Id_station))
    nom_station=c.fetchall()
    conn.close()
    #tracé de la courbe et sauvegarde
    plt.plot(temperature)
    plt.title("Temperature "+T_type+" dans la station de "+str(nom_station[0][0]))
    plt.xlabel("Temps (jour)")
    plt.ylabel("Température en °C)")
    plt.grid(True)
    plt.savefig("D:\ECL\S6\informatique\Projet Application Web\TD4 projet d application web\Courbes\\"+str(new_id)+".png")
    return (new_id)

#Pour avoir le nom de l'image correspondant à ce qu'on veut afficher
def nom_image(Id_station, date_debut,date_fin,T_type):
    conn = sqlite3.connect('graphiques.sqlite')
    c = conn.cursor()
    c.execute("SELECT Id FROM image WHERE Id_station="+str(Id_station)+" AND date_debut="+str(date_debut)+" AND date_fin="+str(date_fin)+" AND T_type='"+T_type+"'")
    Id=c.fetchall()
    conn.close()
    if Id==[]:
        Id=tracer_courbe(Id_station, date_debut,date_fin,T_type)
        return (str(Id)+".png")
    else:
        return (str(Id[0][0])+".png")
    
#permet de déterminer si les données de température existent pour une certaine station.    
def donnees_existantes(Id_station):
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    c.execute("SELECT Id FROM station_meteo s JOIN Temperature t ON s.Id="+str(Id_station)+" AND t.Id_station="+str(Id_station))
    Id=c.fetchone()
    conn.close()
    if Id==None:
        return False
    else:
        return True
        
def coordonnees():
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    c.execute("SELECT Id, Nom_station, Latitude, Longitude FROM station_meteo")
    coordonnees_station = c.fetchall()
    conn.close()
    return coordonnees_station
    
#A=T_station_liste(33,19960719,19990726,'max')

#commande SQL : http://creersonsiteweb.net/page-mysql-sql-select
#python avancé : http://apprendre-python.com/page-creer-graphiques-scientifiques-python-apprendre

#tracer_courbe(33,19960719,19960726,'max')
#print (nom_image(750,19820101,19830201,'min'))

#plt.plot(A[1])
#plt.savefig("D:\ECL\S6\informatique\Projet Application Web\TD4 projet d application web\Courbes\\test.png")

