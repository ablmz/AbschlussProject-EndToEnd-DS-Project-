# End to End Web Scraping-Machine Learning-Deployment Project

This is a Web-DataScience Projekt. This project consists of three parts:

### 1. Web Scraping:
Obtaining reviews from the sites klinikbewertung.de & Google Maps.
The Clinic Datas of 22 Hospitals in Lower Saxony Germany from klinikbewertung.de and Google Maps are scraped. 

#### Framework Google:
- Name of the clinic, textual review, star rating, date of review, likes

#### Framework Klinikbewertungen:
- Name of the clinic, title, date of evaluation, department, star rating (overall satisfaction, quality of advice, medical treatment, administration and processes, equipment and design), experience report

Note: There are ratings for clinic ratings that are not included in the overall ratings (marked on the website and within the HTML document).
Goal: Two files with the respective ratings from Google Maps & clinic ratings for further processing

#### Dependencies:
- Python 3
- Scrapy
- Selenium
- BeatufulSoup
- WebDriver(e.g. ChromeDriver)

### 2. Machine Learning Models and Data Analysis:
Process related & cleaned data using a machine learning method
With using ML methods the data were processed and two different NLP ML Model were created.
We used also Sentiment Analysis(Opnion Mining) as a NLP Method to classify Polarity and Subjectivity of reviews.

#### Model 1:
First of them predicts a review text as good or bad experience
#### Model 2:
Second one predicts the star reviews.

#### Dependencies:
- Pandas
- Numpy
- Matplotlib
- NLTK
- TextBlobDE
- Wordcloud
- Sklearn
- Pickle


### 3. Web Deployment of Model and Analysis Results:
Creating website / web app(with e.g. filter options) to display related data, data analysis and results of machine learning models
We show all Analysis Results and Machine Learning Model Results in a webpage. We used Flask to deploy our ML Models and we prefered http://blitzteam.pythonanywhere.com/

#### Dependencies
- HTML
- CSS
- JS
- Flask
- WebSpace

## Model Deployment and Analysis Results: 
You can visit http://blitzteam.pythonanywhere.com/ to see our Model and Analyse results.

#### Contributors:
- Meryem, Ismail, Asim Irshad, Adem

#### Autor:
- Adem Bilmez
