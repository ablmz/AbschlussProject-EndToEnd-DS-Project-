from slugify import slugify
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