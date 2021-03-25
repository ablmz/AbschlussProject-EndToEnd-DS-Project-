from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

reviews = pd.read_csv("output.csv")
clinics = reviews["Name der Klinik"].unique()

    


@app.route('/')

def index():
    

    return render_template("index.html", clinics=clinics)   

@app.route('/ergebnisse', methods=["GET","POST"])

def ergebnisse():
    select = str(request.form.get("klinikNameList"))
    klinik=reviews.loc[reviews["Name der Klinik"]==select]
    
    kTitle=klinik["Title"]
    print(kTitle)
    kDatum=klinik["Datum der Bewertung"]
    kSterne=klinik["Gesamtzufriedenheit"]
    kPro=klinik["Pro"]
    kKontra=klinik["Kontra"]
    kText=klinik["Erfahrungsbericht"]
    return render_template("ergebnisse.html", clinics=clinics, klinikName=select,  kTitle= kTitle, kDatum=kDatum ) 
    


if __name__=="__main__":
    app.run(debug=True)

#C:/xampp/htdocs/abschluss/Final-Project/web-seite