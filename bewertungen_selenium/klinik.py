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

url = 'https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-tiefenbrunn-rosdorf'

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

reviews = driver.find_elements_by_xpath("//div[@class='list ratinglist']/article")


review_title = driver.find_elements_by_xpath("//header/h2")
review_date = driver.find_elements_by_xpath("//time")
review_text = driver.find_elements_by_xpath("//p[@itemprop='reviewBody']")
treatment_year = driver.find_elements_by_xpath("//div[@class='meta']")

print(treatment_year[0].text)
driver.close()