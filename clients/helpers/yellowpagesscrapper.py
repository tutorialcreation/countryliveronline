import requests
from bs4 import BeautifulSoup


class YellowPagesScrapper:
    def __init__(self) -> None:
        pass

    def extract_details(self):
        base_uri = "http://yellowpageskenya.com"
        base_url = "https://yellowpageskenya.com"
        url = "https://yellowpageskenya.com/search-results?what=restaurant&keywords=restaurant&where=Nairobi"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        links, businesses = [], []
        for x in range(12, 22):
            links.append(
                f"https://yellowpageskenya.com/search-results?page={x}&what=restaurant&where=Nairobi")
        enterprises_ = []
        for link in links:
            print(link)
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            enterprises_.append(soup.find_all('div', class_='results-display'))
        for enterprise in enterprises_:
            for item in enterprise:
                name = item.find('h2', {'itemprop': 'name'}).text
                address = item.find(
                    'span', class_='streetaddress').text.strip().replace('\n', '')
                try:
                    link = item.find('a', class_='bizemail')['href']
                except Exception as e:
                    link = ''
                try:
                    website = item.find('a', class_='bizwebsite')['href']
                except Exception as e:
                    website = ''

                phone_numbers = []
                if "business-email" in link:
                    link = link.replace("business-email", "business-details")
                    link = f"{base_url}{link}"
                    raw = requests.get(link, headers=headers)
                    soup_ = BeautifulSoup(raw.content, 'html.parser')
                    phone_numbers_ = soup_.find_all(
                        "a", class_="dropdown-item secondary")
                    for phone_number in phone_numbers_:
                        phone_numbers.append(phone_number.text)

                business = {
                    'name': name,
                    'address': address,
                    'website': website,
                    'link': link,
                    'phone_numbers': phone_numbers
                }
                businesses.append(business)
