from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from slugify import slugify
import pickle

app = Flask(__name__)


# Bewertungen
k_reviews = pd.read_csv("clinical_data_lowersaxony.csv")
g_reviews = pd.read_csv("clinical_data_lowersaxony_google.csv")

#Vorhersage Model
loaded_vectorizer= pickle.load(open('vectorizer.pickle','rb'))
loaded_model= pickle.load(open('classification.model','rb'))

clinics = g_reviews["Name der Klinik"].unique()

k_klinikInfos=[]
g_klinikInfos=[]

def getGoogleInfos(selected): 
    g_klinik = g_reviews.loc[g_reviews['Name der Klinik'] == selected]
    g = g_klinik[["Titel","Fachbereich","Datum","Erfahrungsbericht",'Gesamtzufriedenheit']]
    for i in range(len(g)):
        info = list(g.iloc[i])
        g_klinikInfos.append(info)
    return g_klinikInfos

def getKlinikInfos(selected): 
    k_klinik = k_reviews.loc[k_reviews['Name der Klinik'] == selected]
    k = k_klinik[["Titel","Fachbereich","Datum","Erfahrungsbericht","Gesamtzufriedenheit"]]
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
        selected = 'Augenklinik Dr.Hoffmann'
        slug_name = slugify(selected)
        k_Infos=getKlinikInfos(selected)
        g_Infos=getGoogleInfos(selected)
        return render_template("ergebnisse.html", clinics=clinics, klinikName=selected, k_Infos=k_Infos,g_Infos=g_Infos, slug_name=slug_name)


  
@app.route('/vorhersage', methods=["GET","POST"])
def vorhersage():
    

    if request.method == 'POST':
        text = request.form.get("comment")
        output = loaded_model.predict(loaded_vectorizer.transform([text]))
        return render_template('vorhersage.html',pred=output)
       
    else:
        return render_template('vorhersage.html')


@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

if __name__=="__main__":
    app.run(debug=True)