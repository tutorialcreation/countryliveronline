import requests
from bs4 import BeautifulSoup


class GoogleMapsApi:
    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def search_clients(self, query):
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name%2Crating%2Cformatted_phone_number&key={self.api_key}"

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        return response.text

    def scrap_links(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        return soup
