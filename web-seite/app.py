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
    gKlinikInfos=[]
    for i in range(len(k)):
        info=list(k.iloc[i])
        gKlinikInfos.append(info)
    return gKlinikInfos

def getInfos(select): 
    klinik=reviews.loc[reviews['Name der Klinik']==select]
    k=klinik[["Title","Pro","Kontra","Erfahrungsbericht","Gesamtzufriedenheit","Datum der Bewertung",'sentimentBewertung']]
    klinikInfos=[]
    for i in range(len(k)):
        info=list(k.iloc[i])
        klinikInfos.append(info)
    return klinikInfos

def getGooglePieChart(select):
    url="../static/img/images/g_piechart/g_p_"+select+".png"
    return url

def getGoogleWordCloud(select):
    url="../static/img/images/g_wordcloud/g_w_"+select+".png"
    return url

def getKlinicWordCloud(select):
    url="../static/img/images/k_wordcloud/k_w_"+select+".png"
    return url

@app.route('/')

def index():
    

    return render_template("index.html", clinics=clinics)   

@app.route('/ergebnisse', methods=["GET","POST"])

def ergebnisse():
    select = str(request.form.get("klinikNameList"))
    
    kInfos=getInfos(select)
    g_p=getGooglePieChart(select)
    g_w=getGoogleWordCloud(select)
    k_w=getKlinicWordCloud(select)
    gInfos=getGoogleInfos(select)
    return render_template("ergebnisse.html", clinics=clinics, klinikName=select, kInfos=kInfos,gInfos=gInfos, gPieChart=g_p, gWordCloud=g_w, kWordCloud=k_w) 
    


if __name__=="__main__":
    app.run(debug=True)

#C:/xampp/htdocs/abschluss/Final-Project/web-seite