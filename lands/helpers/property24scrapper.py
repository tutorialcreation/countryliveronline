import requests
from bs4 import BeautifulSoup


class PropertyScrapper:
    def __init__(self) -> None:
        self.base_url = "https://www.property24.co.ke/"

    def get_links(self):
        r = requests.get(self.base_url+"property-for-sale")
        soup = BeautifulSoup(r.content, "html.parser")
        data = []
        for item in soup:
            try:
                link_div = item.find(
                    'div',{'class':'sc_listingTileContent'}
                )
                link = [a['href'] for a in link_div.find_all('a',href=True)]
            except Exception as err:
                link = None
            try:
                name = item.find(
                    'div', {'class': 'sc_listingTileArea '}).text
            except Exception as err:
                name = None
            try:
                price = item.find(
                    'div', {'class': 'sc_listingTilePrice'}).span.text
            except Exception as err:
                price = None
            try:
                location = item.find(
                    'div', {'class': 'sc_listingTileAddress'}).span.text
            except Exception as err:
                location = None
            try:
                size = item.find(
                    'div', {'class': 'sc_listingTileTeaser'}).span.text
            except Exception as err:
                size = None
            lc = {
                "link":link,
                "name":name,
                "price":price,
                "location":location,
                "size":size

            }
            data.append(
                lc
            )
        print(data)
