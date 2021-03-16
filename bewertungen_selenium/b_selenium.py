import pandas as pd
from slugify import slugify
from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located


url = 'https://www.google.com/maps/place/Asklepios+Hospital+Tiefenbrunn/@51.498851,9.8716437,15z/data=!4m5!3m4!1s0x0:0xd7525199e92be7b!8m2!3d51.498851!4d9.8716437'

# Google Web driver path
chrome_driver_path = "chromedriver"
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


# Number of reviews and scroll number
sleep(2)
reviews_number = driver.find_element_by_xpath('//*[@class="gm2-caption"]').text.split()
scroll_number = (int(reviews_number[0]))//10+1
print(f"Maximum scroll need to get full data: {scroll_number}")

# -------------------------------------------#
# FUNCTION - Scrolling full down to see all reviews
def scroll_review():
	sleep(1)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root"))) # Waits for the page to load.
	x=0
	while (x < int(scroll_number)):
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
sleep(2)
expand_reviews()
#------------------------------------------#
# TEXT REVIEWS SCRAPING - FUNCTION

commentators = driver.find_elements_by_xpath('//div[@class="section-review-title"]/span')
reviews = driver.find_elements_by_xpath('//div[@class="section-review-review-content"]/span[2]')
stars = driver.find_elements_by_xpath('//div[@class="section-review-metadata section-review-metadata-with-note"]/span[2]')
dates = driver.find_elements_by_xpath('//span[@class="section-review-publish-date"]')
likes = driver.find_elements_by_xpath('//span[@class="section-review-thumbs-up-count"]')

infos = []
y=1
while(y<int(reviews_number[0])):
	info = []	
	first_user = commentators.pop(0)
	commentator = first_user.text
	info.append(commentator)
	
	first_review = reviews.pop(0)
	review = first_review.text.replace('\n','**')
	info.append(review)

	first_date = dates.pop(0)
	date = first_date.text
	info.append(date)

	if (len(likes))==0:
		like='No Like'
	else:
		first_like = likes.pop(0)
		like = first_like.text
	info.append(like)

	first_star = stars.pop(0)
	star = first_star.get_attribute("aria-label").split()
	info.append(star[0])

	infos.append(info)

	#user.clear()
	y= y+1
	
#----------------------------------------#
#Creating CSV file with function

def create_csv(csv_name,reviews_list,fields):
	with open(csv_name, 'w', encoding='utf-8') as f:
		# using csv.writer method from CSV package 
		write = csv.writer(f)
		write.writerow(fields)
		write.writerows(reviews_list)

#Clinicks name change into slug value (abc-def-ghi)
csv_name = slugify(klinik_name)+'.csv'

# Columns titles
fields = ['Name', 'Kommanter', 'Datum', 'Like', 'Star']

create_csv(csv_name,infos,fields)

driver.close()
