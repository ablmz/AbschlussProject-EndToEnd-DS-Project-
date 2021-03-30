import pandas as pd
import csv


daten = pd.read_csv("output.csv")
clinics = daten["Name der Klinik"].unique()

def create_csv(csv_name,reviews_list):
	with open(csv_name, 'w', encoding='utf-8') as f:
		# using csv.writer method from CSV package 
		write = csv.writer(f)
		write.writerow(['Klinik_Name'])
		write.writerow(reviews_list)

#Clinicks name change into slug value (abc-def-ghi)
#csv_name = slugify(klinik_name)+'.csv'

# Columns titles
#fields = ['Klinik_Name']

create_csv('k_name.csv',clinics)

