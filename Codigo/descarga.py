# Librerias
import bs4
import requests
import re
from selenium import webdriver


# ---------------- Datos FIFA ---------------------------------
# Obtenemos pagina web

linkFifa = 'http://es.fifa.com/fifa-tournaments/teams/search.html?filter=&btsearch='
pagFifa = requests.get(linkFifa)
contFifa = bs4.BeautifulSoup(pagFifa.text, "lxml")

# Obtenemos nombre de los equipos

contStr = format(contFifa.encode('latin'))
equipos = re.findall('<img alt="([^"\'>]*)', contStr)
equipos = equipos[2:]

# -------------------------------------------------------------

# -------------- Datos FootballDatabase -----------------------


# Funcion descarga

def descarga(equipo):

	# Variables
	numeros = ['1','2','3','4','5','6','7','8','9','0']
	abcMay = ['A', 'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	abcMin = ['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	listaAnos = []
	listaTemp = []
	l = 22

	# Ingresamos e iniciamos sesion en FootballDatabase
	linkFootDb = 'http://www.footballdatabase.eu/'
	#buscador = webdriver.Chrome('/home/khovateky/Documentos/chromedriver')
	buscador = webdriver.PhantomJS()
	buscador.get(linkFootDb)
	usuario =  buscador.find_element_by_name("login")
	usuario.send_keys("PruebaHC")
	clave = buscador.find_element_by_name("password")
	clave.send_keys("herramientasc")
	ingresar = buscador.find_element_by_id("connectu")
	ingresar.click()

	# Ingresamos a equipo especifico
	buscaInterno = buscador.find_element_by_name("seek")
	buscaInterno.send_keys(equipo)
	buscaEquipo = buscador.find_element_by_id("oku")
	buscaEquipo.click()
	aEquipo = buscador.find_element_by_link_text(equipo)
	aEquipo.click()
	aResultados = buscador.find_element_by_id("liencalen")
	aResultados.click()

	# Obtenemos lista de temporadas
	htmlEquipo = buscador.page_source
	htmlEqBS4 = bs4.BeautifulSoup(htmlEquipo, "lxml")
	htmlLista = htmlEqBS4.find_all('select',{'class':'champclassique'})

	for i, ages in enumerate(htmlLista):
		listaAnos += [ages.getText()]
	
	while l < len(listaAnos[0]):
		listaTemp += [listaAnos[0][l:l+4]]
		l += 5

	
	# Obtenemos datos de cada temporada
	for i in range(len(listaTemp)):

		# Obtenemos link de pagina web
		datosEquipo = []
		linkEquipo = buscador.current_url
		linkEquipo = linkEquipo[0:-4]
		linkEquipo = str(linkEquipo) + str(listaTemp[i])

		# Obtenenmos html de la web
		buscador.get(linkEquipo)
		htmlTempEq = buscador.page_source
		htmlTempEqBS4 = bs4.BeautifulSoup(htmlTempEq, "lxml") 
		tablaResult = htmlTempEqBS4.find_all('tr',{'class':'stylemneutre'}) 

		# Obtenemos datos del equipo
		for j,registro in enumerate(tablaResult):
			if "penalties" not in registro.getText() and "Despu" not in registro.getText() and "Previa" not in registro.getText():
				datosEquipo += [registro.getText()] 

		# Reseteamos contador
		d = 0

		for d in range(len(datosEquipo)):	

			# Obtenemos fecha partido y la separamos del resto de datos
			fecha = datosEquipo[d][:13]
			restoDatos = datosEquipo[d][13:]
			
			# Obtenemos competencia
			for c in range(1,len(restoDatos)):
				if restoDatos[c] in abcMay and restoDatos[c-1] in abcMin:
					competencia = restoDatos[:c]
					restoDatos = restoDatos[c:]
					break

			# Descartamos jornada de los datos
			for m in range(1,len(restoDatos)):
				if restoDatos[m] in abcMay and (restoDatos[m-1] in abcMin or restoDatos[m-1] in abcMay or restoDatos[m-1] in numeros):
					restoDatos = restoDatos[m:]
					break

			# Obtenemos los resultados del equipo local y su resultado
			for rl in range(1,len(restoDatos)):
				if restoDatos[rl] in numeros and restoDatos[rl-1] != "-" and restoDatos[rl-2] != "-":
					resultadoLC = restoDatos[rl]
					equipoLC = restoDatos[:rl]
					restoDatos = restoDatos[rl:]
					break

			# Obtenemos los resultados del equipo visitante y su resultado
			for rv in range(2,len(restoDatos)):
				if restoDatos[rv] in numeros and restoDatos[rv-1] != "-" and restoDatos[rv-2] != "-":
					resultadoVS = restoDatos[rv]
					equipoVS = restoDatos[rv+1:]
					break

			# Variable de formato
			encoding = "utf-8"	

			# Ingresamos datos al archivo que contendra la base de datos
			doc.write("|"+format(fecha.encode(encoding))+"|"+format(competencia.encode(encoding))+"|"+format(equipoLC.encode(encoding))+"|"+format(resultadoLC.encode(encoding))+"|"+format(resultadoVS.encode(encoding))+"|"+format(equipoVS.encode(encoding))+"| \n")

	
			

   
	# -------------------------------------------------------------



# Abrimos archivo y escribimos encabezado
doc = open("datos.md","w")
doc.write("| FECHA | TORNEO | LOCAL | GL | GV | VISITANTE | \n")
doc.write("|:---:|:---:|:---:|:---:|:---:|:---:| \n")

# Recorremos lista de equipos y hacemos el proceso de extraccion de datos
for t in range(len(equipos)):
	descarga(equipos[t].decode('utf-8'))
	print t

# Cerramos documento al finalizar la extraccion de datos
doc.close()