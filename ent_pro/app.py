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



clinics = g_reviews["Name der Klinik"].unique()





def getGoogleInfos(selected):
    g_klinikInfos=[] 
    g_klinik = g_reviews.loc[g_reviews['Name der Klinik'] == selected]
    g = g_klinik[["Datum der Bewertung","Textuelle Bewertung","Sternebewertung","Likes","sentimentBewertung","Klinik Name"]]
    #g_klinikName = g[5]  
    for i in range(len(g)):
        info = list(g.iloc[i])
        g_klinikInfos.append(info)
    return g_klinikInfos

def getKlinikInfos(selected):
    k_klinikInfos=[] 
    k_klinik = k_reviews.loc[k_reviews['Name der Klinik'] == selected]
    k = k_klinik[["Titel","Fachbereich","Datum","Erfahrungsbericht","Gesamtzufriedenheit","sentimentBewertung","Klinik Name"]]
    #k_klinikName = k[6]
    #k = k_klinik[["Title","fachbereich","Datum der Bewertung","Erfahrungsbericht","Gesamtzufriedenheit"]]
    for i in range(len(k)):
        info=list(k.iloc[i])
        k_klinikInfos.append(info)
    return k_klinikInfos


@app.route('/')
def index():
    return render_template("index.html", clinics=clinics)
 

@app.route('/ergebnisse', methods=["POST"])
def ergebnisse():

    
    if request.method == 'POST':        
       
        selected = str(request.form.get("klinikNameList"))
        if selected not in clinics:
            return render_template("index.html", message ='Bitte wählen Sie ein Klinik aus',clinics=clinics)

        #slug_name = slugify(selected)
        k_Infos=getKlinikInfos(selected)
        g_Infos=getGoogleInfos(selected)
        klinikName = ''

        

        for k in k_Infos:
            klinikName = k[6]

        return render_template("ergebnisse.html", clinics=clinics, klinikName=selected, k_Infos=k_Infos,g_Infos=g_Infos, slug_name=klinikName)
    else:
        return abort(404, 'Opps! Falsch Vorgang')
   
def sternVorherSage(text):
    #Ster Vorhersage Model
    loaded_vectorizer= pickle.load(open('vectorizer.pickle','rb'))
    loaded_model= pickle.load(open('classification.model','rb'))
    output = loaded_model.predict(loaded_vectorizer.transform([text]))
    output = int(output[0])
    return output

def bewertung(text):
    output1 = 'Gute Erfahrung'
    output2 = 'Schlechte Erfahrung'
    load_vectorizer = pickle.load(open('vector.pickle', 'rb'))

    # load the model
    load_model = pickle.load(open('classifications.model', 'rb'))

    # make a prediction
    if load_model.predict(load_vectorizer.transform([text])):
        #print("Gute Erfahrung")
        return output1
    else:
        #print("Schlechte Erfahrung")
        return output2

@app.route('/vorhersage', methods=["GET","POST"])
def vorhersage():
    

    if request.method == 'POST':
        text = request.form.get("comment")
        # output = loaded_model.predict(loaded_vectorizer.transform([text]))
        # output = int(output[0])
        stern_vorhersage = sternVorherSage(text)
        text_vorhersage = bewertung(text)
        return render_template('vorhersage.html', pred_stern = stern_vorhersage, pred_text = text_vorhersage)
       
    else:
        return render_template('vorhersage.html')

@app.route('/admin')
def admin():
    return redirect('http://www.pythonanywhere.com/login/?next=')

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

if __name__=="__main__":
    app.run(debug=True)