from flask import Flask, render_template, request, url_for, redirect, abort
import pandas as pd
from slugify import slugify
import pickle
# from flask_wtf.csrf import CSRFProtect
# import os

app = Flask(__name__)

# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY
# csrf = CSRFProtect(app)

# Bewertungen
k_reviews = pd.read_csv("clinical_data_lowersaxony_gereinigt.csv")
g_reviews = pd.read_csv("clinical_data_lowersaxony_google_gereinigt.csv")

#Vorhersage Model
loaded_vectorizer= pickle.load(open('vectorizer.pickle','rb'))
loaded_model= pickle.load(open('classification.model','rb'))

clinics = g_reviews["Name der Klinik"].unique()

k_klinikInfos=[]
g_klinikInfos=[]

def getGoogleInfos(selected): 
    g_klinik = g_reviews.loc[g_reviews['Name der Klinik'] == selected]
    g = g_klinik[["Datum der Bewertung","Textuelle Bewertung","Sternebewertung","Likes","sentimentBewertung"]]    
    for i in range(len(g)):
        info = list(g.iloc[i])
        g_klinikInfos.append(info)
    return g_klinikInfos

def getKlinikInfos(selected): 
    k_klinik = k_reviews.loc[k_reviews['Name der Klinik'] == selected]
    k = k_klinik[["Titel","Fachbereich","Datum","Erfahrungsbericht","Gesamtzufriedenheit","sentimentBewertung"]]
    #k = k_klinik[["Title","fachbereich","Datum der Bewertung","Erfahrungsbericht","Gesamtzufriedenheit"]]
    for i in range(len(k)):
        info=list(k.iloc[i])
        k_klinikInfos.append(info)
    return k_klinikInfos

@app.route('/')
def index():
    return render_template("index.html", clinics=clinics)
 
@app.route('/ergebnisse', methods=["GET","POST"])
def ergebnisse():
    
    if request.method == 'POST':    

        selected = str(request.form.get("klinikNameList"))
        if selected not in clinics:
            return render_template("index.html", message ='Bitte wählen Sie ein Klinik aus',clinics=clinics)

        slug_name = slugify(selected)
        k_Infos=getKlinikInfos(selected)
        g_Infos=getGoogleInfos(selected)
        return render_template("ergebnisse.html", clinics=clinics, klinikName=selected, k_Infos=k_Infos,g_Infos=g_Infos, slug_name=slug_name)
    else:
        return abort(404, 'Opps! Falsch Vorgang')
        
        # return render_template("index.html", message ='Bitte wählen Sie ein Klinik aus',clinics=clinics)
    #     selected = 'Augenklinik Dr.Hoffmann'
    #     slug_name = slugify(selected)
    #     k_Infos=getKlinikInfos(selected)
    #     g_Infos=getGoogleInfos(selected)
    #     return render_template("ergebnisse.html", clinics=clinics, klinikName=selected, slug_name=slug_name)
        


  
@app.route('/vorhersage', methods=["GET","POST"])
def vorhersage():
    

    if request.method == 'POST':
        text = request.form.get("comment")
        output = loaded_model.predict(loaded_vectorizer.transform([text]))
        output = int(output[0])
        return render_template('vorhersage.html',pred=output)
       
    else:
        return render_template('vorhersage.html')


@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

if __name__=="__main__":
    app.run(debug=True)