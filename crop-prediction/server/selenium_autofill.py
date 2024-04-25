from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import time
import time
from time import sleep
import pandas as pd
import math
from random import randint

from selenium.common.exceptions import NoSuchElementException
from pymongo import DESCENDING, MongoClient


def webpagecompleteloaded(driver):
    return driver.execute_script("return document.readyState") == "complete"


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# Function to check if an element is visible
def is_element_visible(element):
    return element.is_displayed()


# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# MongoDB URI
uri = "mongodb+srv://Shivam:Shivam@agriculture.y46nprf.mongodb.net/?retryWrites=true&w=majority&appName=Agriculture"

# Connect to the MongoDB server
client = MongoClient(uri)
import random


while True:
    # Access the 'agridata' database
    db = client.agridata
    # Access the 'parameter' collection
    collection = db.parameter
    # Fetch the last inserted document
    last_inserted_document = collection.find_one(sort=[("_id", DESCENDING)])

    # Print the last inserted document
    # print("Last Inserted Document:")
    # print(last_inserted_document)
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-gpu")
    s = Service("C:\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()

    driver.get("http://localhost:3000/")

    # Wait until the page is completely loaded
    while not webpagecompleteloaded(driver):
        time.sleep(4)
        print("Waiting for page to load")
    print(last_inserted_document)
    # Define the values to input
    # Generate random values for each variagenerate_random_values()

    inputs = {
        "nitrogen": last_inserted_document["Nitrogen"],  # example value for nitrogen
        "nitrogen2": last_inserted_document["Nitrogen"],  # example value for nitrogen
        "phosphorus": last_inserted_document["Phosphorous"],
        "potassium": last_inserted_document["Potassium"],  # example value for potassium
        "phosphorus2": last_inserted_document["Phosphorous"],
        "potassium2": last_inserted_document["Potassium"],
        "moisture2": last_inserted_document["Moisture"],  # example value for moisture
        "ph": last_inserted_document["pH"],  # example value for pH
    }

    # Locate each input field by its name attribute and entethe defined values
    for key, value in inputs.items():
        input_element = driver.find_element("name", key)
        input_element.clear()  # Clear any pre-filled values
        input_element.send_keys(value)
    # Find the button by XPath and click it
    button = driver.find_element(
        By.XPATH, "/html/body/div/div/div/section[2]/div/div[2]/form/button"
    )
    button.click()
    time.sleep(5)

    button = driver.find_element(
        By.XPATH, "/html/body/div/div/div/section[3]/div/div[1]/form/button"
    )
    button.click()
    time.sleep(8)

    # time.sleep(35)
