from bs4 import BeautifulSoup
import requests
from csv import writer




url = 'https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-soltau'
r = requests.get(url)
r.encoding='utf-8'
print(r)
soup = BeautifulSoup(r.text,"html.parser")

# All reviews

count=1
for a in soup.find_all('article',class_ = "bewertung"):
    bewertung = a.text.rstrip().lstrip()
    print('\n+++++++++++++++++++' ,(count), 'REVIEW +++++++++++++++++++')
    print(bewertung)
    count+=1






