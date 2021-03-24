import numpy as np
import pandas as pd
import textblob
from textblob_de import TextBlobDE
import matplotlib.pyplot as plt

file =r"C:\Users\nutzer\Desktop\Projekt\Final\Webscrapping_Github\Machine_Learning _Google_reviews\ggl_scrap_allurl_22.csv"
df = pd.read_csv(file)
df=pd.DataFrame(df)

# print(df.isnull().sum()) # checking if some cells have null values

df["Textuelle_Bewertung"].fillna("No Review",inplace =True)  # Replaceing none values 
df=df.replace(['Marienkrankenhaus Papenburg- Aschendorf GmbH Betriebsstätte Aschendorf'],'Marienkrankenhaus-Aschendorf') # shortening name
df=df.replace(['Klinikum Emden - Hans-Susemihl-Krankenhaus'],'Klinikum Emden') # shortening name

# print(df.isnull().sum())  # checking if all values are there
graph=[]
kname=[]
for i,j in zip(df.Name_der_Klinik.unique(),df.Textuelle_Bewertung):
    print(i) 
    blob = TextBlobDE(j)
    feedback=blob.sentiment.polarity
    # print(feedback)
    if feedback == 0:
        print('      ///// Netrual Sentiment /////')
    elif feedback > 0:
        print('      +++++ Positive Sentiment +++++')
    else:
        print ('      ----- NEGATIVE SENTIMENT -----')
    print('')
    graph.append(feedback)      # adding results in graph list
    kname.append(i)             # adding all clinic names in kname list
# print(graph)


plt.bar(kname, height=graph, align='center', width=0.4)
plt.xticks(fontsize=10, rotation=90)                    # rotating the name 90 degree
plt.title('SENTIMENT ANALYSIS of Google map reviews of 22 Hospitals')
plt.xlabel("Name der Klinik")
plt.ylabel("Sentiment Analyze")
mng = plt.get_current_fig_manager()
mng.window.showMaximized()          # maximizing the window
plt.tight_layout() 
plt.subplots_adjust(bottom=0.4)     #  adjust as it was cutting names
plt.show()