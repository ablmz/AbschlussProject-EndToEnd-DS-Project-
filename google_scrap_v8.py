import pandas as pd
from time import sleep
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located


url = 'https://www.google.com/maps/place/Heidekreis-Klinikum+GmbH+Krankenhaus+Soltau/@52.9894409,9.847291,15z/data=!3m1!4b1!4m8!1m2!11m1!2s1tsS4C8icZfBtXgqho9ekuv3aB34!3m4!1s0x47b1b'

# Google Web driver path
chrome_driver_path = "/Users/nutzer/Desktop/Projekt/Final/Webscrapping_Github/chromedriver.exe"
chrome_options = Options()

#  To hide the Chrome browser
Options.headless = False   
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

driver.get(url)
sleep(5)
driver.maximize_window()
wait = WebDriverWait(driver,10)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="consent-bump"]/div/div[1]/iframe')))  
agree = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span'))) 
agree.click()


# Clicking on Search button
sleep(5)
suche = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
sleep(3)
suche.click()
sleep(10)

# Printing clinic name
klinik_name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
print(klinik_name)

# Clicking more reviews
all_review = driver.find_element_by_class_name('widget-pane-link')
all_review.click()

bewertungen_anzahl = (all_review.text).split()
scroll_anzahl = (int(bewertungen_anzahl[0]))//10+1
print(f"Maximum scroll need to get full data: {scroll_anzahl}")


# -------------------------------------------#
# FUNCTION - Scrolling full down to see all reviews
def scroll_review():
	sleep(1)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root"))) # Waits for the page to load.
	x=0
	while (x < scroll_anzahl):
		scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show') # It gets the section of the scroll bar.
		print( '  ', x+1, '  times scroll')
		sleep(2)
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div) # Scroll it to the bottom.
		x=x+1

	else:	
		print('')

# RECALLNG - SCROLL FUNCTION
sleep(5)
scroll_review()


# -------------------------------------------#
# EXPANDING REVIEWS - FUNCTION
def expand_reviews():
	expand = driver.find_elements_by_class_name("section-expand-review")

	for i in expand:
		i.click()

# RECALLNG - EXPANDING ALL REVIEWS FUNTION
print('\nExpanding Review...\n')
sleep(2)
expand_reviews()


# -------------------------------------------#
# TEXT REVIEWS SCRAPING - FUNCTION
def text_reviews():
	t_reviews = driver.find_elements_by_class_name("section-review-review-content")
	txt_review=[]

	for i in t_reviews:
		txt_review.append(i.text.strip())
	return(txt_review)
		# print('---------')

# RECALLNG TEXT REVIEWS FUNCTION
# text_reviews()


# -------------------------------------------#
# COUNT - TOTAL NUMBER OF REVIEWS - FUNCTION
t_reviews = driver.find_elements_by_class_name("section-review-review-content")
print('Total number of reviews are ',len(t_reviews))


# -------------------------------------------#
# STAR REVIEWS SCRAPING - FUNCTION
def star_reviews():
	s_reviews = driver.find_elements_by_css_selector("[class='section-review-stars']")
	
	star_reviews_list = []
	
	for a in s_reviews:
		star_reviews_list.append(a.get_attribute("aria-label"))
	return(star_reviews_list)
	

# RECALLNG STAR REVIEWS FUNTION
# star_reviews()


# -------------------------------------------#
# DATE OF REVIEWS SCRAPING - FUNCTION

def date_reviews():
	date_reviews = driver.find_elements_by_css_selector("[class='section-review-publish-date']")
	datum_list =[]
	for i in date_reviews:
		datum_list.append(i.text)
	
	return(datum_list)

# RECALLNG DATE OF REVIEWS FUNTION
# dreviews = date_reviews()


# -------------------------------------------#
# NUMBER OF LIKES SCRAPING - FUNCTION
def total_likes():
	
	t_reviews = driver.find_elements_by_class_name("section-review-review-content")	# Retreiving TOTAL NUMBER OF REVIEWS including without Likes button option
	t_like = driver.find_elements_by_class_name("section-review-interactions-label") # Retreiving total number of LIKES
	likes_list=[]
	for i in t_reviews:		 #This loop will make the default value of likes list to zero
		likes_list.append(0)

	Likes_len = (len(likes_list))		#Total length of list
	
	digit=0
	while (digit < Likes_len) :		# Loop for replacing the default value (0) in list
	
		for l in t_like:
			lk=(l.text).strip()
			if lk != 'Teilen':
				if lk =='Gefällt mir' or '':
					lk = 0
				else:
					lk=lk

				likes_list[digit]=lk
				digit=digit+1
		
		return(likes_list)				

# RECALLNG NUMBER OF LIKE FUNTION
# total_likes()


# -------------------------------------------#
# WRITING IN CSV - EXCEL FORM

print ('\nAdding data in a CSV file...\n')

df = pd.DataFrame(
	{'Name der Klinik': klinik_name,
	'Sternbewertung':star_reviews(), 
	'Datum der Bewertung': date_reviews(),
	'Likes':total_likes(),
	 'Textuelle Bewertung': text_reviews()	 
	})



datei='/Users/nutzer/Desktop/Projekt/Final/Webscrapping_Github/new_scrap.csv'
df.to_csv(datei, index=False, mode='a', header=True, encoding="utf-8")

driver.close()