import bs4
import requests


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
	teams[i] = format(teams[i].encode("latin")).lower()

else:
    print "Error al cargar la pagina"
    


print teams[9]
    
