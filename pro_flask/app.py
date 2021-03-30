from flask import Flask, render_template, request, url_for
import pandas as pd
from slugify import slugify

app = Flask(__name__)

daten = pd.read_csv("output.csv")
klinikInfos=[]

def getInfos(select): 
    klinik=daten.loc[daten['Name der Klinik']==select]
    k=klinik[["Title","Pro","Kontra","Erfahrungsbericht","Gesamtzufriedenheit","Datum der Bewertung"]]
    for i in range(len(k)):
        info=list(k.iloc[i])
        klinikInfos.append(info)
    return klinikInfos

clinics = daten["Name der Klinik"].unique()
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        clinic_name = request.form.get('clinic_name')
        image = slugify(clinic_name)+'.png'
        return render_template("index.html", clinics=clinics, image=image )
    else:
        return render_template("index.html", clinics=clinics)



@app.route('/ergebnisse', methods=["GET","POST"])
def ergebnisse():
    select = str(request.form.get("clinic_name"))
    
    kInfos=getInfos(select)
    return render_template("ergebnisse.html", clinics=clinics, klinikName=select, kInfos=kInfos ) 
    

if __name__ == '__main__':
    app.run()