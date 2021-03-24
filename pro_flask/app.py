from flask import Flask, render_template, request, url_for
import pandas as pd
from slugify import slugify

app = Flask(__name__)

daten = pd.read_csv("output.csv")


@app.route('/', methods=['GET', 'POST'])
def index():
    clinics = daten["Name der Klinik"].unique()
    if request.method == 'POST':
        clinic_name = request.form.get('clinic_name')
        image = slugify(clinic_name)+'.png'
        return render_template("index.html", clinics=clinics, image=image )
    else:
        return render_template("index.html", clinics=clinics)


if __name__ == '__main__':
    app.run()