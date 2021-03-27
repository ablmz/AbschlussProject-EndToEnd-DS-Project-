from flask import Flask, render_template, request,url_for,redirect
import os
import pandas as pd

app = Flask(__name__)

reviews = pd.read_csv("output.csv")
gDatai=pd.read_csv("ggl_scrap_allurl_22.csv")

clinics = reviews["Name der Klinik"].unique()
klinikInfos=[]
gKlinikInfos=[]

def getGoogleInfos(select): 
    gklinik=gDatai.loc[gDatai["Name_der_Klinik"]==select]
    k=gklinik[["Sternbewertung","Textuelle_Bewertung","Likes","Datum_der_Bewertung",'sentimentBewertung']]
    for i in range(len(k)):
        info=list(k.iloc[i])
        gKlinikInfos.append(info)
    return gKlinikInfos

def getInfos(select): 
    klinik=reviews.loc[reviews['Name der Klinik']==select]
    k=klinik[["Title","Pro","Kontra","Erfahrungsbericht","Gesamtzufriedenheit","Datum der Bewertung",'sentimentBewertung']]
    for i in range(len(k)):
        info=list(k.iloc[i])
        klinikInfos.append(info)
    return klinikInfos


@app.route('/')

def index():
    

    return render_template("index.html", clinics=clinics)   

@app.route('/ergebnisse', methods=["GET","POST"])

def ergebnisse():
    select = str(request.form.get("klinikNameList"))
    
    kInfos=getInfos(select)
    gInfos=getGoogleInfos(select)
    return render_template("ergebnisse.html", clinics=clinics, klinikName=select, kInfos=kInfos,gInfos=gInfos ) 
    


if __name__=="__main__":
    app.run(debug=True)

#C:/xampp/htdocs/abschluss/Final-Project/web-seite