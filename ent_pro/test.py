import pandas as pd
from slugify import slugify
import pickle


loaded_vectorizer= pickle.load(open('vectorizer.pickle','rb'))
loaded_model= pickle.load(open('classification.model','rb'))


text = "Einer der schlechtesten und inkompetentesten Menschen die ich in einem Krankenhaus gesehen und erlebt habe! Man wird behandelt wie der letzte dreck und noch dazu sind die Mitarbeiter mehr als Inkompetent und haben noch nie etwas von Freundlichkeit gehört!!! Trotz der schwierigen Zeit kann es nicht angehen so behandelt zu werden und mit Menschen zu umzugehen! Der Oberarzt in der Anästhesie müsste fristlos gekündigt werden das letzte was ihm am Herzen liegt ist es Menschen zu helfen! Er ist zu überfordert in seiner Position!"

output = loaded_model.predict(loaded_vectorizer.transform([text]))
# print(loaded_model.predict(loaded_vectorizer.transform([text])))

print(output)