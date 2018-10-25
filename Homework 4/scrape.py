# Homework 4 - Scraper
# Using this guide: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

# import libraries
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import re
import requests

resp = requests.get("https://www.alexa.com/topsites/category/Top/Games")
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding, features="lxml")

urlList = []
cleanUrlList = []

for link in soup.find_all('a', href=True):
    print(link['href'])
    urlList.append(link['href'])

for url in urlList:
    if ("/siteinfo/" in url):
        url = url = re.sub('/siteinfo/', '', url)
        cleanUrlList.append(url)

print (cleanUrlList)

