from bs4 import BeautifulSoup
import requests
from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

url = 'https://www.google.com/maps/place/Herzogin+Elisabeth+Hospital/@52.2329937,10.5267147,15z/data=!4m5!3m4!1s0x0:0x66131345a9ba3dfe!8m2!3d52.2329937!4d10.5267147'

# r = requests.get(url)
# r.encoding='utf-8'
# soup = BeautifulSoup(r.text,"html.parser") 

# Google Web driver path
chrome_driver_path = "chromedriver"
chrome_options = Options()

#  To hide the Chrome browser
Options.headless = False   
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

driver.get(url)
sleep(2)
driver.maximize_window()
# sleep(5)

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

bewertungen = (all_review.text).split()
scroll_ren = (int(bewertungen[0]))//10+1
print(scroll_ren)

# FUNCTION Scrolling full down to see all reviews
def scroll_review():
	sleep(1)
	x=0
	while (x < scroll_ren):
		scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show') # It gets the section of the scroll bar.
		print( '  ', x, '  times scroll')
		sleep(5)
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div) # Scroll it to the bottom.
		x=x+1

	else:	
		print('end if statement')


# RECALLNG SCROLL FUNCTION
scroll_review()

results = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[10]')

print(results.text)

driver.close()
