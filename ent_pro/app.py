from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from slugify import slugify

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

k_reviews = pd.read_csv("clinical_data_lowersaxony.csv")
g_reviews = pd.read_csv("clinical_data_lowersaxony_google.csv")


clinics = k_reviews["Name der Klinik"].unique()

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
        slug_name = slugify(selected)
        k_Infos=getKlinikInfos(selected)
        g_Infos=getGoogleInfos(selected)
        return render_template("ergebnisse.html", clinics=clinics, klinikName=selected, k_Infos=k_Infos,g_Infos=g_Infos, slug_name=slug_name)

# @app.route('/<string:data>', methods=["GET","POST"])
# def vorhersage(data):
    
#     if request.method == 'POST':
#         data = 'Vorhersage ok oldu mu acaba'
#         data = slugify(data)     
#         return redirect(url_for('vorhersage', data=data))
    
@app.route('vorhersage', methods=["GET","POST"])
def vorhersage():
     if request.method == 'POST':
         
        comment = str(request.form.get("comment"))
        
        prediction = model.predict_proba(comment)

        output=prediction[0]


        return render_template('vorhersage.html',pred='Your probability of diabetes is % {}'.format(output))

         


if __name__=="__main__":
    app.run(debug=True)