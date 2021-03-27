import numpy as np
import pandas as pd
import textblob
from textblob_de import TextBlobDE
import matplotlib.pyplot as plt
from PIL import Image
import time
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS

file =r"C:\Users\nutzer\Desktop\Projekt\Final\Webscrapping_Github\Machine_Learning _Google_reviews\ggl_scrap_allurl_22.csv"
df = pd.read_csv(file)
df=pd.DataFrame(df)



# print(df.isnull().sum()) # checking if some cells have null values

df["Textuelle_Bewertung"].fillna(" ",inplace =True)  # Replaceing none values 

# Changing Name GOOGLE MAPS REVIEW name as in KLINIKBEWERTUNGEN.de

df=df.replace(['Augenklinik Dr. Hoffmann'],'Augenklinik - Dr. Hoffmann') # 1 shortening name
df=df.replace(['Krankenhaus Marienstift gGmbH'],'Krankenhaus der evangelisch-lutherischen Diakonissenanstalt Marienstift') #  2 shortening name
df=df.replace(['Herzogin Elisabeth Hospital'],'HEH Herzogin Elisabeth Hospital') # 3 shortening name
df=df.replace(['Asklepios Fachklinikum Göttingen'],'Asklepios Fachklinikum Göttingen') # 4 shortening name
df=df.replace(['Asklepios Fachklinikum Tiefenbrunn'],'Asklepios Fachklinikum Tiefenbrunn') # 5 shortening name
df=df.replace(['DIAKOVERE Friederikenstift'],'DIAKOVERE Friederikenstift') # 6 shortening name
df=df.replace(['DIAKOVERE Annastift'],'DIAKOVERE Annastift') # 7 shortening name
df=df.replace(['DRK-Krankenhaus Clementinenhaus'],'DRK-Clementinenhaus') # 8 shortening name
df=df.replace(['Sophienklinik GmbH'],'Sophienklinik GmbH') # 9 shortening name
df=df.replace(['KRH Klinikum Großburgwedel'],'KRH Klinikum Großburgwedel') # 10 shortening name
df=df.replace(['KRH Klinikum Lehrte'],'KRH Klinikum Lehrte') # 11 shortening name
df=df.replace(['Krankenhaus Lindenbrunn'],'Krankenhaus Lindenbrunn') # 12 shortening name
df=df.replace(['Sana Klinikum Hameln-Pyrmont'],'Sana Klinikum Hameln-Pyrmont') # 13 shortening name
df=df.replace(['AMEOS Klinikum Alfeld'],'Kreis- und Stadtkrankenhaus Alfeld') # 14 shortening name
df=df.replace(['Helios Klinikum Hildesheim'],'HELIOS Klinikum Hildesheim GmbH') # 15 shortening name
df=df.replace(['HELIOS Klinik Cuxhaven'],'HELIOS Klinik Cuxhaven') # 16 shortening name
df=df.replace(['OsteMed Klinik Bremervörde'],'Ostemed Klinik Bremervörde') # 17 shortening name
df=df.replace(['Klinik Fallingbostel'],'Klinik Fallingbostel') # 18 shortening name
df=df.replace(['Klinikum Emden - Hans-Susemihl-Krankenhaus'],'Klinikum Emden') # 19 shortening name
df=df.replace(['Krankenhaus Ludmillenstift'],'Krankenhaus Ludmillenstift') # 20 shortening name
df=df.replace(['Marienkrankenhaus Papenburg- Aschendorf GmbH Betriebsstätte Aschendorf'],'Marien Hospital Papenburg-Aschendorf') # 21 shortening name
df=df.replace(['Kreiskrankenhaus Osterholz'],'Kreiskrankenhaus Osterholz') # 22 shortening name


# print(df.isnull().sum())  # checking if all values are there

# print(df)





for k in df.Name_der_Klinik.unique():
    print(k)
    ein_k_bewertung = df["Textuelle_Bewertung"].loc[df['Name_der_Klinik'] == k]
        
    
    time.sleep(2)
    
    '''


    ####   word cloud ###  

    ein_k_bewertung = str(ein_k_bewertung)
    print(ein_k_bewertung)

    x, y = np.ogrid[:1000, :1000]
    mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
    mask = 255 * mask.astype(int)   
    # STOPWORDS.update(["dtype"])
    german_stop_words = stopwords.words('german')
    german_stop_words.append('dtype')
    german_stop_words.append('Textuelle_Bewertung')
    german_stop_words.append('object')

    wordcloud = WordCloud(stopwords=german_stop_words, background_color="white",width=1920, height=1080, mask=mask).generate(ein_k_bewertung.lower()) #width=1920, , height=1080

    plt.imshow(wordcloud, extent=(8, 70, 8, 70), interpolation="bilinear")
    plt.axis("off")
    plt.rcParams['figure.figsize'] = [12, 18]
    plt.savefig("C:/Users/nutzer/Desktop/Projekt/Final/Webscrapping_Github/Machine_Learning _Google_reviews/images/wordcloud/"+"g_w_" + k + ".png", dpi=300)
    # plt.show()




    '''


    sehr_gut=0
    gut=0
    neutral = 0
    schlecht =0
    sehr_schlecht= 0
    
    for ein in ein_k_bewertung:
        blob = TextBlobDE(ein)
        pol = blob.sentiment.polarity
        # print(ein)
#         print(pol)

        if pol >= 0.5 and pol <=1:
            sehr_gut += 1
            
        elif pol > 0 and pol < 0.5 :
            gut += 1
            
        elif pol == 0 :
            neutral += 1
            
        elif pol < 0 and pol >= (-0.5) :
            schlecht += 1
            
        else:
            sehr_schlecht += 1
            
#     print(sehr_gut)
#     print(gut)
#     print(neutral)
#     print(schlecht)
#     print(sehr_schlecht)
    
    share=[]
    share.append(sehr_gut)
    share.append(gut)
    share.append(neutral)
    share.append(schlecht)
    share.append(sehr_schlecht)
    print(share)
    
    wert =['Sehr Gut', 'Gut', 'Neutral(incl. no review)', 'Schlecht', 'Sehr Schlecht']
    comp = pd.DataFrame({"share" : share, "wert" : wert})
    ax = comp.plot(y="share", kind="pie", labels = comp["wert"], autopct = '%1.0f%%', legend=False, title=k+'  - \nVerteilungprozent der Kommentare')

    # Hide y-axis label
    ax.set(ylabel='')
    # plt.show()
    plt.savefig("C:/Users/nutzer/Desktop/Projekt/Final/Webscrapping_Github/Machine_Learning _Google_reviews/images/piechart/"+"g_p_" + k + ".png", dpi=300)
