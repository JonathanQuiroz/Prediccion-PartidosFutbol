#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bs4
import requests
from selenium import webdriver
import time

url = "http://es.fifa.com/fifa-tournaments/teams/search.html"
req = requests.get(url)
teams = []
statusCode = req.status_code
if statusCode == 200:
    html = bs4.BeautifulSoup(req.text, "lxml") 
    entradas = html.find_all('span',{'class':'team-name'})
    for i,entrada in enumerate(entradas):
        entrada.encode("utf-8")
        t = entrada.getText()
        teams += [t]
	teams[i] = format(teams[i].encode("latin"))
else:
    print "Error al cargar la pagina"

# Funcion para llegar hasta los datos de el equipo necesario

def descarga(team):
    
    abcmay = ['A', 'B','C','D','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    abcmin = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    doc = open("datos.md","w")
    doc.write("| EQUIPO | FECHA | TORNEO | LOCAL | GL | GL | VISITANTE | \n")
    doc.write("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n")
    
    #browser = webdriver.PhantomJS()
    browser = webdriver.Chrome('/home/khovateky/Documentos/chromedriver')
    browser.get('http://www.footballdatabase.eu/')
    time.sleep(2)
    txtusername = browser.find_element_by_name("login")
    txtpassword = browser.find_element_by_name("password")
    txtusername.send_keys("PruebaHC")
    txtpassword.send_keys("herramientasc")
    btnsigin = browser.find_element_by_id("connectu")
    btnsigin.click()

    # Buscamos equipo necesario

    txtsearch = browser.find_element_by_name("seek")
    txtsearch.send_keys(team.decode('utf-8'))
    btnsearch = browser.find_element_by_id("oku")
    btnsearch.click()

    # Accedemos a pagina del equipo

    team = browser.find_element_by_link_text(team.decode('utf-8'))
    team.click()

    # Accedemos a los resultados 

    result = browser.find_element_by_id("liencalen")
    result.click()

    # Tomo la lista de años de los que hay datos del equipo
    codpage = browser.page_source
    time.sleep(2)
    listage = []

    html = bs4.BeautifulSoup(codpage, "lxml") 
    entradas = html.find_all('select',{'class':'champclassique'})


    for i,entrada in enumerate(entradas):
        entrada.encode("utf-8")
        t = entrada.getText()
        listage += [t]


    listmod =  listage[0][22:]
    i = 0
    listafinal = []

    while i < len(listmod):
        listafinal += [listmod[i:i+4]]
        i += 5

    # Obtenemos datos de equipo segun el año

    urlteam = browser.current_url
    urlteam = urlteam[0:-4]


    for i in range(2,len(listafinal)):
        urlteam = str(urlteam) + str(listafinal[i])

        
        browser.get(urlteam)
        obtpage = browser.page_source
        
        pageteam = bs4.BeautifulSoup(obtpage, "lxml") 
        tablaresult = pageteam.find_all('tr',{'class':'stylemneutre'})

        datos = []

        for j,entrada in enumerate(tablaresult):
                datos += [entrada.getText()]
                
                for k in range(len(datos)):
                
                    # Fecha del partido
                    fecha = datos[k][:12]

                    # Obtengo posicion del equipo local
                    posteam = datos[k].find(str(team).decode('utf-8'))

                    # Obtengo el grupo y torneo
                    gruptor = datos[k][12:posteam]

                    # -------------------------------------------------------------------------------
                    # --------------------------------------- Datos cuando es local -----------------

                    try:
                        # Obtengo resultados equipos
                        teamsresult =  datos[k][posteam:].split(" ")

                        # Obtengo nombre equipo local
                        teamloc = teamsresult[0]

                        # Obtengo posicion de competicion
                        for l in range(1,len(gruptor)):
                            if gruptor[l] in abcmay and gruptor[l-1] in abcmin:
                                posfincom = l
                                break

                        # Obtengo competicion
                        comp = gruptor[1:posfincom]


                        # Obtengo resultados y visitante
                        prueba = teamsresult[1].split("\n")

                        # Resultados equipo local
                        resultlocal = prueba[0]

                        # Obtengo visitante y competicion
                        for n in range(len(prueba[1])):
                            if prueba[1][n] in abcmay:
                                posvis = n
                                break

                        # Obtengo equipo visitante
                        teamvis = prueba[1][posvis:]

                        # Obtengo resultado equipo visitante
                        resultvis = prueba[1][:posvis]

                    except IndexError:
                    # -------------------------------------------------------------------------------
                    # --------------------------------------- Datos cuando es visitante -------------
                        # Obtengo nombre visitante
                        teamvis = datos[k][posteam:]

                        # Busco posicion de la competencia
                        for m in range(1,len(gruptor)):
                            if gruptor[m] in abcmay and gruptor[m-1] in abcmin:
                                break


                        comp = gruptor[1:m]
                        gruptor = gruptor[m:]

                        # Busco posicion del equipo local
                        for o in range(1,len(gruptor)):
                            if gruptor[o] in abcmay and (gruptor[o-1] in abcmay or gruptor[o-1] in abcmin):
                                break

                        # Ajustes para hallar los resultados
                        prueba = gruptor[o:].split(" ")
                        teamloc = prueba[0]
                        resultados = prueba[1].split("\n")
                        resultlocal = resultados[0]
                        resultvis = resultados[1]
                        
                        print team,fecha,comp,teamloc,resultlocal,resultvis, teamvis

                        
                        doc.write("|"+format(str(team).encode('ascii', 'ignore'))+"|"+format(str(fecha).encode('ascii', 'ignore'))+"|"+format(str(comp).encode('ascii', 'ignore'))+"|"+format(str(teamloc).encode('ascii', 'ignore'))+"|"+format(str(resultlocal).encode('ascii', 'ignore'))+"|"+format(str(resultvis).encode('ascii', 'ignore'))+"|"+format(str(teamvis).encode('ascii', 'ignore'))+"|\n")
    doc.close()
    
descarga("Colombia")

print "¡Todo esta listo!"
