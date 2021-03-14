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

# -------------------------------------------#
# FUNCTION - Scrolling full down to see all reviews
def scroll_review():
	# try:
	# 	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root"))) # Waits for the page to load.
	x=1
	while (x < 11):
		scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show') # It gets the section of the scroll bar.
		print( '  ', x, ' x scrolling down')
		sleep(2)
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div) # Scroll it to the bottom.
		x=x+1

	else:	
		print('')

# RECALLNG - SCROLL FUNCTION
sleep(2)
scroll_review()

# -------------------------------------------#
# EXPANDING REVIEWS - FUNCTION
def expand_reviews():
	expand = driver.find_elements_by_class_name("section-expand-review")

	for i in expand:
		i.click()

# RECALLNG - EXPANDING ALL REVIEWS FUNTION
sleep(2)
expand_reviews()

# -------------------------------------------#
# TEXT REVIEWS SCRAPING - FUNCTION
def text_reviews():
	t_reviews = driver.find_elements_by_class_name("section-review-review-content")

	for i in t_reviews:
		print(i.text.strip(),'\n')

# RECALLNG TEXT REVIEWS FUNTION
text_reviews()


# -------------------------------------------#
# STAR REVIEWS SCRAPING - FUNCTION
def star_reviews():
	s_reviews = driver.find_elements_by_css_selector("[class='section-review-stars']")
	star_reviews_list = []

	for s in s_reviews:
		star_reviews_list.append(s.get_attribute("aria-label"))
	for i in star_reviews_list:
		print(i)

# RECALLNG STAR REVIEWS FUNTION
star_reviews()

# -------------------------------------------#
# DATE OF REVIEWS SCRAPING - FUNCTION
def date_reviews():
	date_reviews = driver.find_elements_by_css_selector("[class='section-review-publish-date']")

	for i in date_reviews:
		print(i.text)

# RECALLNG DATE OF REVIEWS FUNTION
date_reviews()

