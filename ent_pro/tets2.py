import pickle

def Bewertung(text):
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

result = Bewertung('Einfach Schlecht')
print(result)