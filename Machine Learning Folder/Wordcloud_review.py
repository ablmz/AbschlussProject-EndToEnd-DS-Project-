import numpy as np
import pandas as pd
# import textblob
# from textblob import TextBlob
from textblob_de import TextBlobDE
# from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")



file =r"C:\Users\nutzer\Desktop\Projekt\Final\Webscrapping_Github\Machine_Learning _Google_reviews\ggl_scrap_allurl_22.csv"
df = pd.read_csv(file)
df=pd.DataFrame(df)

# print(df.isnull().sum()) # checking if some cells have null values

df["Textuelle_Bewertung"].fillna("No Review",inplace =True)  # Replaceing none values 
df=df.replace(['Marienkrankenhaus Papenburg- Aschendorf GmbH Betriebsstätte Aschendorf'],'Marienkrankenhaus-Aschendorf') # shortening name
df=df.replace(['Klinikum Emden - Hans-Susemihl-Krankenhaus'],'Klinikum Emden') # shortening name

# print(df.isnull().sum())  # checking if all values are there

pos_list=[]

for i,j in zip(df.Name_der_Klinik.unique(),df.Textuelle_Bewertung):
    # print(i)
    blob = TextBlobDE(j)
    t = blob.tags
    # print(t)
    for tag in t:
        if tag[1] == 'JJ':
            pos_list.append(tag[0])
# print(str(pos_list))

wordcloud = WordCloud(width = 1200, height = 600, min_font_size = 10, background_color ='white').generate(str(pos_list))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()          
