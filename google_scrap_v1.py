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


url = 'https://www.google.com/maps/place/Heidekreis-Klinikum+GmbH+Krankenhaus+Soltau/@52.9894409,9.847291,15z/data=!3m1!4b1!4m8!1m2!11m1!2s1tsS4C8icZfBtXgqho9ekuv3aB34!3m4!1s0x47b1b'

r = requests.get(url)
r.encoding='utf-8'
soup = BeautifulSoup(r.text,"html.parser") 

# Google Web driver path
chrome_driver_path = "/Users/nutzer/Desktop/Projekt/Final/Webscrapping_Github/chromedriver.exe"
chrome_options = Options()

#  To hide the Chrome browser
Options.headless = False   
# chrome_options.add_argument("--headless")

webdriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

webdriver.get(url)
sleep(2)
webdriver.maximize_window()
sleep(5)
wait = WebDriverWait(webdriver,10)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="consent-bump"]/div/div[1]/iframe')))  
agree = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span'))) 
agree.click()

# Clicking on Search button
sleep(5)
suche = webdriver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
sleep(3)
suche.click()
sleep(10)

# webdriver.close()