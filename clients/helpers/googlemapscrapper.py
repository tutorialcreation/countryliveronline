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


class GoogleMapScrapper:
    def __init__(self) -> None:
        self.base_url = "https://www.google.com/maps/search/{0}/@{1},{2},16z"
        self.json_file_path = settings.BASE_DIR + "/clients/data/"
        self.delay = 10

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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                  options=chrome_options)
        driver.get(url)
        html_data = []
        try:
            # wait for button to be enabled
            WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'section-result'))
            )
            driver.implicitly_wait(40)

            html = driver.find_element(
                By.TAG_NAME, 'html').get_attribute('innerHTML')
            html_data.append(html)
        except Exception as err:
            logging.error(err)
        else:
            logging.info('getting html')
            html = driver.page_source
            html_data.append(html)
        finally:
            driver.quit()
        print(html_data[0])
        return html_data[0]

    def get_details(self, search: str, city: str):
        soup = BeautifulSoup(self.get_html(search, city))
        results = soup.find_all('div', {'class': 'section-result'})
        data = []
        for item in results:
            try:
                name = item.find('h3').span.text
            except Exception as err:
                name = None
            try:
                rating = item.find(
                    'span', {'class': 'cards-rating-score'}).text
            except Exception as err:
                rating = None
            try:
                num_reviews = item.find(
                    'span', {'class': 'section-result-num-ratings'}).text
            except Exception as err:
                num_reviews = None
            try:
                cost = item.find('span', {'class': 'section-result-cost'}).text
            except Exception as err:
                cost = None
            try:
                tags = item.find(
                    'span', {'class': 'section-result-details'}).text
            except Exception as err:
                tags = None
            try:
                addr = item.find(
                    'span', {'class': 'section-result-location'}).text
            except Exception as err:
                addr = None
            try:
                descrip = item.find(
                    'div', {'class': 'section-result-description'}).text
            except Exception as err:
                descrip = None
            data.append({'name': name, 'rating': rating, 'num_revs': num_reviews,
                         'cost': cost, 'tags': tags, 'address': addr,
                         'description': descrip, })
        temp_df = pd.DataFrame(data)
        return temp_df
