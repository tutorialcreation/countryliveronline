from django.shortcuts import render
from django.views.generic import View
import requests
from bs4 import BeautifulSoup

# Create your views here.


class YellowPagesScrapperView(View):
    def post(self, request, *args, **kwargs):
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
        return render(request, 'clients/yellowpages.html')


class FacebookScrapperView(View):
    def get(self, request, *args, **kwargs):
        token = "EAAIh96UqoXMBAIZCprokyrdA8rVsnGLKKQCPB9t4pJNzm7p4tQ6GqLGfcZAvDt4ngZBddR7HrYuEOoW10oromn4C8HQuLhCQhRVqw72HpFN9TVTdzSRXmvHPJ7nZBbxS7gJ6KMNuCk4PLZBZCY56JbulKgiAYepYXYyBNSphERoCz5u5QwjbLoVzR3x3oGVoZCJou3ZBRiBjmAZDZD"
        url = f"https://graph.facebook.com/search?q=restaurant&type=place&center=40.714623,-74.006605&distance=16000&access_token={token}"

        r = requests.get(
            "https://www.google.com/maps/search/restaurants+in+nairobi/@-1.2830089,36.8077103,15z/data=!3m1!4b1")
        soup = BeautifulSoup(r.content, "lxml")
        a = soup.prettify()
        return render(request, 'clients/facebook.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'clients/facebook.html')
