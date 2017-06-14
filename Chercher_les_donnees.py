# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 12:23:58 2017

@author: Guillaume Touzé
"""

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
#from pylab import plot.savefig

#repertoire_image="D:\ECL\S6\informatique\Projet Application Web\TD4 projet d application web\Courbes\"

plusieurs_courbes=True  #variable globale permettant de savoir si on veut tracer des courbes de plusieurs stations en même temps 

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
def tracer_courbe(Id_station, date_debut,date_fin,T_type,datedebutsav,datefinsav):
    assert donnees_existantes(Id_station)==True
    valeurs=T_station_liste(Id_station, date_debut,date_fin,T_type)
    #création de la liste des temps au format JJ/MM/AAAA
    temps=valeurs[0]
    for i in range(len(temps)):
        temps[i]=date_claire(temps[i])
    temps=np.array(temps)
    temperature=np.array(valeurs[1])
    #Accès au nom de la station
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    c.execute("SELECT Nom_station FROM station_meteo WHERE Id="+str(Id_station))
    nom_station=c.fetchall()
    conn.close()
    #Création de la légende
    legende="Temperature "+T_type+" dans la station de "+str(nom_station[0][0])
    #Ajout de l'image dans la base de données
    conn = sqlite3.connect('graphiques.sqlite')
    c = conn.cursor()
    c.execute("SELECT MAX(Id) FROM image")
    maxi_id=c.fetchall()
    new_id= maxi_id[0][0]+1
    c.execute("INSERT INTO image VALUES ("+str(new_id)+","+str(Id_station)+",'"+T_type+"',"+str(date_debut)+ ","+str(date_fin)+",'"+legende+"')")
    conn.commit()
    conn.close()
    #tracé de la courbe et sauvegarde
    plt.plot(temperature)
    plt.xlabel("Temps (jour)")
    plt.ylabel("Température (en °C)")
    L=np.linspace(0,len(temps),10,endpoint=True)
    L=[int(i) for i in L]
    L[-1]=L[-1]-1
    tps=[temps[i] for i in L]
    plt.xticks(L,tps)
    print(L)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig("client/Courbes/"+str(Id_station)+str(datedebutsav)+str(datefinsav)+str(T_type)+".png")
    plt.close()
    return (new_id,"Temperature "+T_type+" dans la station de "+str(nom_station[0][0]))

#Pour afficher plusieurs courbes
def tracer_courbe_plu(Id_station, date_debut,date_fin,T_type):       #Id_station est une liste
    #assert donnees_existantes(Id_station)==True
    n=len(Id_station)
    #création de la liste des temps au format JJ/MM/AAAA
    temps=T_station_liste(Id_station[0], date_debut,date_fin,T_type)[0]
    for i in range(len(temps)):
        temps[i]=date_claire(temps[i])
    temps=np.array(temps)
    #Rajout des températures
    temperature=[]
    for i in range(n):
        temperature.append(np.array(T_station_liste(Id_station[i], date_debut,date_fin,T_type)[1]))
    #Accès au nom de la station
    nom_station=[]
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    for i in range(n):
        c.execute("SELECT Nom_station FROM station_meteo WHERE Id="+str(Id_station[i]))
        nom_station.append(c.fetchall())
    conn.close()
    #Création de la légende
    if n==1:
        legende="Temperature "+T_type+" dans la station de "+str(nom_station[0][0])
    else:
        legende="Temperature "+T_type+" dans la station de "
        for i in range(n):
            if i==(n-1):
                legende=legende[:-1]
                legende=legende+"et "+nom_station[i][0][0]+"."
            else:
                legende=legende+nom_station[i][0][0]+","
    #Ajout de l'image dans la base de données
    conn = sqlite3.connect('graphiques.sqlite')
    c = conn.cursor()
    c.execute("SELECT MAX(Id) FROM image")
    maxi_id=c.fetchall()
    new_id= maxi_id[0][0]+1
    id_tot=""
    for i in range(n):
        id_tot=id_tot+str(Id_station[i])
    c.execute("INSERT INTO image VALUES ("+str(new_id)+","+str(id_tot)+",'"+T_type+"',"+str(date_debut)+ ","+str(date_fin)+",'"+legende+"')")
    conn.commit()
    conn.close()
    #tracé de la courbe et sauvegarde
    for i in range(n):
        plt.plot(temperature[i], label = "hehe" )#nom_station[i][0][0])
    plt.xlabel("Temps (jour)")
    plt.ylabel("Température (en °C)")
    L=np.linspace(0,len(temps),10,endpoint=True)
    L=[int(i) for i in L]
    L[-1]=L[-1]-1
    tps=[temps[i] for i in L]
    plt.xticks(L,tps)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig("client/Courbes/"+str(id_tot)+str(date_debut)+str(date_fin)+str(T_type)+".png", dpi= 100)
    return (new_id,legende)    
    
#Pour avoir le nom de l'image correspondant à ce qu'on veut afficher
def nom_image(Id_station, date_debut,date_fin,T_type):
    conn = sqlite3.connect('graphiques.sqlite')
    c = conn.cursor()
    c.execute("SELECT Id, legende FROM image WHERE Id_station="+str(Id_station)+" AND date_debut="+str(date_debut)+" AND date_fin="+str(date_fin)+" AND T_type='"+T_type+"'")
    Id=c.fetchall()
    conn.close()
    if Id==[]:
        Id_et_legende=tracer_courbe(Id_station, date_debut,date_fin,T_type)
        return (str(Id_et_legende[0])+".png",Id_et_legende[1])
    else:
        print (Id)
        return (str(Id)+".png", Id)
    
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
        
#Permet de renvoyer la liste des stations météo avec leur propriétés
def coordonnees():
    conn = sqlite3.connect('meteo.sqlite')
    c = conn.cursor()
    c.execute("SELECT Id, Nom_station, Latitude, Longitude FROM station_meteo")
    coordonnees_station = c.fetchall()
    conn.close()
    return coordonnees_station

#Pour transformer une date au format AAAAMMJJ au format JJ/MM/AAAA
def date_claire(date):
    date=str(date)
    return date[6:8]+"/"+date[4:6]+"/"+date[:4]
    
#A=T_station_liste(33,19960719,19990726,'max')

#commande SQL : http://creersonsiteweb.net/page-mysql-sql-select
#python avancé : http://apprendre-python.com/page-creer-graphiques-scientifiques-python-apprendre

#print (nom_image(33,20080719,20090726,'max'))
#print (nom_image(750,19820101,19830201,'min'))
print (tracer_courbe_plu([33,750], 20090719,20090726,'max'))

#plt.plot(A[1])
#plt.savefig("D:\ECL\S6\informatique\Projet Application Web\TD4 projet d application web\Courbes\\test.png")

