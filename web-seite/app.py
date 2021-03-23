from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

reviews = pd.read_csv("output.csv")

@app.route('/')

def index():
    clinics = reviews["Name der Klinik"].unique()

    return render_template("index.html", clinics=clinics)   

if __name__=="__main__":
    app.run(debug=True)