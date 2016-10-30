#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bs4
import requests
from selenium import webdriver

# Obtenemos nombres de los equipos

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

# Ingresamos a FootballDatabase

#browser = webdriver.PhantomJS()
browser = webdriver.Chrome("/home/khovateky/Documentos/chromedriver")
browser.get('http://www.footballdatabase.eu/')
txtusername = browser.find_element_by_name("login")
txtpassword = browser.find_element_by_name("password")
txtusername.send_keys("PruebaHC")
txtpassword.send_keys("herramientasc")
btnsigin = browser.find_element_by_id("connectu")
btnsigin.click()

# Buscamos equipo necesario

txtsearch = browser.find_element_by_name("seek")
txtsearch.send_keys(teams[1].decode('utf-8'))
btnsearch = browser.find_element_by_id("oku")
btnsearch.click()

# Accedemos a pagina del equipo

team = browser.find_element_by_link_text(teams[1].decode('utf-8'))
team.click()

# Accedemos a los resultados 

result = browser.find_element_by_id("liencalen")
result.click()

# Tomo la lista de años de los que hay datos del equipo
codpage = browser.page_source
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
    
print listafinal

    



    


    



    

