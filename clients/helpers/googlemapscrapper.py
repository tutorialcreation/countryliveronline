import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import logging
from time import sleep


class GoogleMapScrapper:
    def __init__(self) -> None:
        self.base_url = "https://www.google.com/maps/search/{0}/@{1},{2},16z"
        self.json_file_path = settings.BASE_DIR + "/clients/data/"
        self.delay = 5

    def get_city(self, city: str, json_file: str):
        df = pd.read_json(self.json_file_path + json_file)
        try:
            xs = df.loc[df['place'].str.contains(
                city.capitalize()), 'latitude'].tolist()
            ys = df.loc[df['place'].str.contains(
                city.capitalize()), 'longitude'].tolist()
            result = (xs[0], ys[0])
        except Exception as e:
            logging.error(e)

        return result

    def get_html(self, search: str, city: str):
        xs, ys = self.get_city(city, "cities.json")
        url = self.base_url.format(search, xs, ys)
        delay = self.delay
        driver_location = "/usr/bin/chromedriver"
        binary_location = "/usr/bin/google-chrome"
        chrome_options = Options()
        chrome_options.binary_location = binary_location
        driver = webdriver.Chrome(executable_path=driver_location,
                                  options=chrome_options)
        driver.get(url)
        print(url)
        WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]'))
        )
        driver.implicitly_wait(40)

        html = driver.find_element(
            By.TAG_NAME, 'html').get_attribute('innerHTML')
        driver.quit()
        return html

    def get_client_details(self, url):
        delay = self.delay
        driver_location = "/usr/bin/chromedriver"
        binary_location = "/usr/bin/google-chrome"
        chrome_options = Options()
        chrome_options.binary_location = binary_location
        driver = webdriver.Chrome(executable_path=driver_location,
                                  options=chrome_options)
        driver.get(url)
        print(url)
        WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[7]/button/div[1]/div[2]/div[1]'))
        )
        driver.implicitly_wait(40)

        html = driver.find_element(
            By.TAG_NAME, 'html').get_attribute('innerHTML')
        phone_number = driver.find_element(
            By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[7]/button/div[1]/div[2]/div[1]')
        driver.quit()
        return html, phone_number

    def get_details(self, search: str, city: str):
        html = self.get_html(search, city)
        soup = BeautifulSoup(html)
        results = soup.find_all('div', {'class': 'Nv2PK THOPZb CpccDe'})

        links = []
        for item in results:
            try:
                a = item.find('a', href=True)
                if a:
                    link = a['href']
                print(link)
            except Exception as err:
                link = None

            links.append({'link': link})

        details = []
        for unscrapped_link in links:
            html, phone_number = self.get_client_details(
                unscrapped_link['link'])
            soup = BeautifulSoup(html)
            results = soup.find_all('div', {'class': 'm6QErb'})
            for item in results:
                try:
                    name = item.find(
                        'h1', {'class': 'DUwDvf fontHeadlineLarge'}).span.text
                except Exception as err:
                    name = None
                try:
                    rating = item.find(
                        'div', {'class': 'fontDisplayLarge'}).text
                except Exception as err:
                    rating = None
                try:
                    num_reviews = item.find(
                        'button', {'class': 'HHrUdb fontTitleSmall rqjGif'}).text
                except Exception as err:
                    num_reviews = None
                try:
                    phone_number = phone_number.text
                except Exception as err:
                    phone_number = None

                details.append({'name': name, 'rating': rating, 'num_revs': num_reviews,
                                'phone_number': phone_number})
                print(details)
        temp_df = pd.DataFrame(details)
        return temp_df
