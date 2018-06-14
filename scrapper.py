#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by P. Renee Carnley for CSC 842 Green Team Cycle 5  #
# Scrapper is a simiple web scrapig tool to gather web files #
# ****DISCLAIMER - author is not responsible for illegal use  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from bs4 import BeautifulSoup
import os
import requests
import sys

website = sys.argv[1] #set varioble website to user defined website
webpage = requests.get(website, timeout=5) #attempt to download website & load response

tempname = website.split(".")

if webpage.status_code == 200:
    soup = BeautifulSoup(webpage.content, 'html.parser')

    filename = "\\" + tempname[1] + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(str(soup))

    print ('Successfully downloaded ' + website)
    data = webpage.text
    soup = BeautifulSoup(data, "lxml")
    for link in soup.find_all('a'):
        print(link.get('href'))
else:
    print('Unable to download ' + website + ' with error code ' + webpage.status_code)

#print(webpage.content)
