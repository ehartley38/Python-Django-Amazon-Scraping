#Contains all logic to do with searching amazon

import requests
from bs4 import BeautifulSoup
import re

URL = 'https://www.amazon.co.uk/Logitech-Wireless-Lightweight-Programmable-compatible/dp/B07CGPZ3ZQ/ref=sr_1_1?dchild=1&keywords=gaming+mouse+wireless&qid=1591273150&refinements=p_89%3ALogitech&rnid=1632651031&sr=8-1'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}



class Product:

    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.user = None


def gather_info(url):
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text().strip()

    try:
        price = float(re.sub('[£]', '', soup2.find(id='priceblock_ourprice').get_text().strip()))
    except AttributeError:
        try:
            price = float(re.sub('[£]', '', soup2.find(id='priceblock_saleprice').get_text().strip()))
        except AttributeError:
            price = float(re.sub('[£]', '', soup2.find(id='priceblock_dealprice').get_text().strip()))



    product = Product(title, price)
    return product

def get_price(url):
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    try:
        price = float(re.sub('[£]', '', soup2.find(id='priceblock_ourprice').get_text().strip()))
    except AttributeError:
        try:
            price = float(re.sub('[£]', '', soup2.find(id='priceblock_saleprice').get_text().strip()))
        except AttributeError:
            try:
                price = float(re.sub('[£]', '', soup2.find(id='priceblock_dealprice').get_text().strip()))
            except:
                #If item at the url no longer exists, then return false
                return False

    return price


