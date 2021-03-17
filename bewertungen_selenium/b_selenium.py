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

kliniks = ['https://www.google.com/maps/place/Augenklinik+Dr.+Hoffmann/@52.2555789,10.5275976,15z/data=!4m2!3m1!1s0x0:0xe66ee9e189648187?sa=X&ved=2ahUKEwiUrOzD5_DuAhVLDOwKHUVOACkQ_BIwDHoECBgQBQ',
'https://www.google.com/maps/place/Krankenhaus+Marienstift+gGmbH/@52.2584042,10.5452332,15z/data=!4m2!3m1!1s0x0:0x2f02bc5a88d3c4a4?sa=X&ved=2ahUKEwiaitH85_DuAhXEwQIHHblHCPkQ_BIwCnoECBUQBQ',
'https://www.google.com/maps/place/Herzogin+Elisabeth+Hospital/@52.2329937,10.5267147,15z/data=!4m2!3m1!1s0x0:0x66131345a9ba3dfe?sa=X&ved=2ahUKEwjDndeY6PDuAhUOwKQKHQttAAkQ_BIwDXoECBoQBQ',
'https://www.google.com/maps/place/Asklepios+Fachklinikum+G%C3%B6ttingen/@51.5241467,9.916557,15z/data=!4m5!3m4!1s0x0:0xa2869d54b7ca1a8a!8m2!3d51.5241467!4d9.916557',
'https://www.google.com/maps/place/Asklepios+Fachklinikum+Tiefenbrunn/@51.498851,9.8716437,15z/data=!4m2!3m1!1s0x0:0xd7525199e92be7b?sa=X&ved=2ahUKEwiLwKW37PDuAhVCC-wKHb2GAFwQ_BIwDXoECBcQBQ',
'https://www.google.com/maps/place/DIAKOVERE+Friederikenstift/@52.3712581,9.7241985,15z/data=!4m2!3m1!1s0x0:0x2562020c6992a2f5?sa=X&ved=2ahUKEwjz4Mm_7PDuAhUJOuwKHfjwDoYQ_BIwDXoECBkQBQ',
'https://www.google.com/maps/place/DIAKOVERE+Annastift/@52.3697126,9.8095478,15z/data=!4m2!3m1!1s0x0:0xcda40e96bf4ee3b5?sa=X&ved=2ahUKEwju-snN7PDuAhUH3KQKHTmUADsQ_BIwCnoECB0QBQ',
'https://www.google.com/maps/place/DRK-Krankenhaus+Clementinenhaus/@52.3867053,9.7451748,15z/data=!4m2!3m1!1s0x0:0xc26fce799779eb2a?sa=X&ved=2ahUKEwi5nJDV7PDuAhUEwQIHHSapBl4Q_BIwCnoECBcQBQ',
'https://www.google.com/maps/place/Sophienklinik+GmbH/@52.3622984,9.7773725,15z/data=!4m2!3m1!1s0x0:0xa5f9e423a2b06584?sa=X&ved=2ahUKEwiDzZqV7fDuAhWKtqQKHdBRAK4Q_BIwDXoECBkQBQ',
'https://www.google.com/maps/place/KRH+Klinikum+Gro%C3%9Fburgwedel/@52.49634,9.86174,15z/data=!4m2!3m1!1s0x0:0x6097ffe5c867564f?sa=X&ved=2ahUKEwiX7YOl7fDuAhXEDOwKHXe_Ax4Q_BIwFnoECCEQBQ',
'https://www.google.com/maps/place/KRH+Klinikum+Lehrte/@52.37997,9.9836,15z/data=!4m2!3m1!1s0x0:0xcdad104f265200f7?sa=X&ved=2ahUKEwjPteLO7fDuAhWOzaQKHaAUCiMQ_BIwDnoECBYQBQ',
'https://www.google.com/maps/place/Krankenhaus+Lindenbrunn/@52.1096994,9.5498324,15z/data=!4m2!3m1!1s0x0:0x2ba194a9d9fbed1d?sa=X&ved=2ahUKEwiqp6iV7_DuAhWN16QKHRgrBg0Q_BIwDXoECBYQBQ',
'https://www.google.com/maps/place/Sana+Klinikum+Hameln-Pyrmont/@52.1072071,9.3519386,15z/data=!4m2!3m1!1s0x0:0x38c5edd92206a8ed?sa=X&ved=2ahUKEwigqvKp7_DuAhXVOuwKHcvCCogQ_BIwDXoECBoQBQ',
'https://www.google.com/maps/place/AMEOS+Klinikum+Alfeld/@51.9942339,9.8324207,15z/data=!4m2!3m1!1s0x0:0xae524284e15399f3?sa=X&ved=2ahUKEwiI24i57_DuAhXGuaQKHcSQAesQ_BIwDHoECBkQBQ',
'https://www.google.com/maps/place/Helios+Klinikum+Hildesheim/@52.15131,9.9766266,15z/data=!4m2!3m1!1s0x0:0x6f9974ba52e7ae71?sa=X&ved=2ahUKEwick53v7_DuAhWPG-wKHeLfAwkQ_BIwDXoECBcQBQ',
'https://www.google.com/maps/place/AGAPLESION+EV.+KLINIKUM+SCHAUMBURG+gGmbH/@52.2648061,9.1052392,15z/data=!4m2!3m1!1s0x0:0xbb35614cf4b2be1?sa=X&ved=2ahUKEwiV0oq18PDuAhWPO-wKHca5CmoQ_BIwCnoECBcQBQ',
'https://www.google.com/maps/place/HELIOS+Klinik+Cuxhaven/@53.8528608,8.6921898,15z/data=!4m2!3m1!1s0x0:0x3a2fe1f38b90ded1?sa=X&ved=2ahUKEwjA0ofu8PDuAhVCPuwKHV3mAX0Q_BIwCnoECBkQBQ',
'https://www.google.com/maps/place/OsteMed+Klinik+Bremerv%C3%B6rde/@53.47135,9.13539,15z/data=!4m2!3m1!1s0x0:0x9e67a0479524aff6?sa=X&ved=2ahUKEwjbvs7z8fDuAhXaOewKHb8_C-cQ_BIwDXoECBgQBQ',
'https://www.google.com/maps/place/Klinik+Fallingbostel/@52.86903,9.7059601,15z/data=!4m2!3m1!1s0x0:0xdc98c5fc80626f15?sa=X&ved=2ahUKEwiYmdaV8vDuAhWCHewKHabKBksQ_BIwE3oECB8QBQ',
'https://www.google.com/maps/place/Klinikum+Emden+-+Hans-Susemihl-Krankenhaus/@53.3754445,7.2129241,15z/data=!4m2!3m1!1s0x0:0x5db7edd86596419e?sa=X&ved=2ahUKEwiDpfyV9PDuAhWCjaQKHWgBCcwQ_BIwD3oECCMQBQ',
'https://www.google.com/maps/place/Krankenhaus+Ludmillenstift/@52.688896,7.2928619,15z/data=!4m2!3m1!1s0x0:0x59c2048e1a4953f?sa=X&ved=2ahUKEwigpYag9vDuAhWxwAIHHXwPDugQ_BIwDXoECBYQBQ',
'https://www.google.com/maps/place/Marienkrankenhaus+Papenburg-+Aschendorf+GmbH+Betriebsst%C3%A4tte+Aschendorf/@53.05092,7.3292999,15z/data=!4m5!3m4!1s0x0:0x20891ebe2b01a054!8m2!3d53.05092!4d7.3292999',
'https://www.google.com/maps/place/Kreiskrankenhaus+Osterholz/@53.2337217,8.7942051,15z/data=!4m2!3m1!1s0x0:0xee4b35384cb3b2ad?sa=X&ved=2ahUKEwjYrbHu8fDuAhVRyaQKHSREAa0Q_BIwDXoECBYQBQ',
'ttps://www.google.com/maps/place/Heidekreis-Klinikum+GmbH+Krankenhaus+Soltau/@52.9894409,9.847291,15z/data=!3m1!4b1!4m8!1m2!11m1!2s1tsS4C8icZfBtXgqho9ekuv3aB34!3m4!1s0x47b1b']

i = 9
url = kliniks[i]

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
	#sleep(1)
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
sleep(3)
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
	info.append(klinik_name)
	first_commentator = commentators.pop(0)
	commentator = first_commentator.text
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
fields = ['Klinik_Name','Commentator', 'Review', 'Date', 'Like', 'Star']

create_csv(csv_name,infos,fields)

driver.close()
