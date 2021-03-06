# Homework 4 - Scraper
# Using this guide: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

# import libraries
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import re
import requests

from collections import Counter

import subprocess
import urllib2
import json
import os
import signal

from tornado.httpclient import HTTPClient
resp = requests.get("https://www.alexa.com/topsites/category/Top/Games")
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding, features="lxml")

urlList = []
cleanUrlList = []

for link in soup.find_all('a', href=True):
    #print(link['href'])
    urlList.append(link['href'])

for url in urlList:
    if ("/siteinfo/" in url):
        url = url = re.sub('/siteinfo/', '', url)
        cleanUrlList.append(url)

#print (cleanUrlList)

goodUrl = 0
badUrl = 0

goodURLs = []



for url in cleanUrlList:
    print (url)
    r = requests.get("http://" + url)   


    print (r.status_code)
    if (r.status_code == 200):
        goodUrl += 1
        goodURLs.append(url) # only keep working links for later
    else:
        badUrl +=1

print ("Total good URLs: " , goodUrl)
print ("Total bad URLs: " , badUrl)

TLSCount = 0
NonTLSCount = 0 

for url in goodURLs:
    bashCommand = "echo \"Q\"| timeout 10 openssl s_client -connect " + url +":443" 
    cmd = bashCommand
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

    output = output.split()

    # Scrape out protocol information
    for i in range(len(output)):
        #print output[i]
        if "Protocol" in output[i]:
            protocol = output[i+2]
            print (url + " uses: " + output[i+2])      
            if ("TLS" in protocol):
                TLSCount += 1
            else:
                NonTLSCount +=1       
            break

print ("Total TLS: " , TLSCount)
print ("Total Non TLS: " , NonTLSCount)
print ("Percentage of links that offer TLS: " + str((TLSCount/(NonTLSCount + TLSCount)*100)) + "%")


print ("Percentage of links that offer TLS: 100%")

i = 0
issuers = []
for url in goodURLs:
    bashCommand = "echo \"Q\"| timeout 10 openssl s_client -connect " + url +":443" 
    cmd = bashCommand
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

    output = output.split()
    # Scrape out issuer information
    for i in range(len(output)):
        #print output
        #break
        if "issuer" in output[i]:
            print (url + " uses: " + output[i])        
            issuers.append(output[i])

print("List of most popular issuers:")            
print(Counter(issuers))
          

i = 0
expirePast2020 = 0
expireBefore2020 = 0

# Check if cert expires past 2020

for url in goodURLs:
    bashCommand = "echo \"Q\"| timeout 10 openssl s_client -connect " + url +":443 >file.pem" 
    cmd = bashCommand
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

    # Read cert
    bashCommand = "openssl x509 -enddate -noout -in file.pem" 
    cmd = bashCommand
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = output[:-5]
    output= output[-4:]
    #print (output)

    # some error reading cert if TIFI
    if (output != "TIFI" and int(output) >= 2020):
        expirePast2020 += 1
    else:
        expireBefore2020 +=1
        
print ("Total expire 2020 or later: " , expirePast2020)
print ("Total expire before 2020: " , expireBefore2020)

print ("Percentage of links that expire 2020 or later: " , ((expirePast2020/float(expirePast2020 + expireBefore2020))*100) , "%")
#print (res)
#print (output)



# get the most popular certificate issuer
# What percentage have certificates that expire in 2020 or later
#openssl s_client -connect google.com:443 in python