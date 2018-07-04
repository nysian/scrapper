#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by P. Renee Carnley for CSC 842 Green Team Cycle 8 #
# Scrapper is a simiple web scraping tool to gather web files #
# ****DISCLAIMER - author is not responsible for illegal use  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from bs4 import BeautifulSoup
import os
import pathlib
import requests
import sys
import tkinter as tk

#Check if webpage request succeeded
def iswebStatusOk(webpageurl):
    if webpageurl.status_code == 200:
        return True
    else:
        print('Unable to download ' + website + ' with error code ' + webpageurl.status_code)
        return False

#check if Directory exists
#if it does not exist create directory
def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    website = sys.argv[1] #set varioble website to user defined website
    webpage = requests.get(website, timeout=5) #attempt to download website & load response

    tempname = website.split(".") #break url into an array get name of website
    websiteName = tempname[1] #get the name of website
    filepath = 'C:\\' + websiteName #set filepath name with website name
    directory = os.path.dirname(filepath) #set directory path with website name

    #check directory & create it with website name
    createDirectory(directory)


    if iswebStatusOk(webpage):
        #get robots.txt files
        robotstxt = webpage + '\\robots.txt'

        if iswebStatusOK(robotstxt):
            soup = BeautifulSoup(robotstxt.content, 'html.parser')
            print soup
        else:
            print





    #check if webpage request succeeded
    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.content, 'html.parser')

        filename = filepath + "\\" + tempname[1] + ".txt"

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
