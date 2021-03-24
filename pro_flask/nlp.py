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

data = pd.read_csv("output.csv")

df = pd.DataFrame(data)

clinic_name = "AGAPLESION EV. KLINIKUM SCHAUMBURG"

review = df.groupby("Name der Klinik")["Erfahrungsbericht"].get_group(clinic_name)

w_cloud_name = slugify(clinic_name)

# erfahrunsberichten=""
# for review in erfahrunsberichten:
#     erfahrunsberichten+= review


result = review.tolist()

#convert list to string and generate

unique_string=(" ").join(result)
blob = TextBlobDE(unique_string)

result = blob.tokens
german_stop_words = stopwords.words('german')

filtered_sentence = [] 
  
for w in result: 
    if w not in german_stop_words: 
        filtered_sentence.append(w)

result=(" ").join(filtered_sentence)
wordcloud = WordCloud(background_color="white",width = 500, height = 500).generate(result)
# plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("static/images/"+w_cloud_name +".png", bbox_inches='tight')
plt.show()
plt.close()

# print(result)