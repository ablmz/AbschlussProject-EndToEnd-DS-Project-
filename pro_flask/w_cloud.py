import pandas as pd
import numpy as np
import csv
import textblob
from textblob_de import TextBlobDE
from textblob_de import PatternParser

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from slugify import slugify




df = pd.DataFrame(pd.read_csv("output.csv"))

def get_wcloud(df,name):

    reviews = df.groupby("Name der Klinik")["Erfahrungsbericht"].get_group(name)

    w_cloud_name = slugify(name)

    result = reviews.tolist()

    #convert list to string and generate

    blob_string=(" ").join(result)
    blob = TextBlobDE(blob_string)
    result = blob.tokens
    result = result.lower()
    german_stop_words = stopwords.words('german')

    filtered_sentence = [] 
  
    for w in result: 
        if w not in german_stop_words: 
            filtered_sentence.append(w)

    result2=(" ").join(filtered_sentence)
    wordcloud = WordCloud(background_color="white",width = 500, height = 500).generate(result2)
    # plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("static/images/"+w_cloud_name +".png", bbox_inches='tight')
    # plt.show()
    plt.close()

clinics = df["Name der Klinik"].unique()

for clinic in clinics:
    get_wcloud(df,clinic)

# print(stopwords.words('german'))