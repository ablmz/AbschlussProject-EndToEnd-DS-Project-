from bs4 import BeautifulSoup
import requests
from csv import writer

url = 'https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-soltau'
r = requests.get(url)
r.encoding='utf-8'
soup = BeautifulSoup(r.text,"html.parser")      

file= open('webscrapping.csv','w')
writer = writer(file)
header = ['Name der Klinik','Titel','Datum der Bewertung','Fachbereich','Gesamtzufriedenheit', 'Qualität der Beratung', 'Mediz. Behandlung', 'Verwaltung und Abläufe', 'Ausstattung und Gestaltung', 'Erfahrungsbericht']

writer.writerow(header)

review = soup.find_all('article',class_ = "bewertung")
klinik_name = soup.find('h1').text.strip()

for i in review:    
    titel = i.find('h2').text.strip()
    datum = i.find('time').text.strip()
    fach = i.find(class_='right').text.strip()
    
    writer.writerow([klinik_name,titel,datum,fach])
    