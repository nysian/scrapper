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

def writeFile(content, file, permission):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, permission, encoding="utf-8") as f:
        f.write(str(content))

def readFile(file):
    array = []
    try:
        sites = open(file)
        for line in sites.read().split():
            array.append(line)
        return array
    except IOError:
        print("File not found")

def main():
    sitefile = sys.argv[1] #get file path
    websites = readFile(sitefile) #set array websites to the user defined ones from given file

    i = 0
    while i < len(websites):
        try:
            website = str(websites[i])
            webpage = requests.get(website, timeout=5) #attempt to download website & load response

            tempname = website.split(".") #break url into an array get name of website
            websiteName = tempname[1] #get the name of website
            filepath = 'C:\\' + websiteName #set filepath name with website name
            directory = os.path.dirname(filepath) #set directory path with website name

            #check directory & create it with website name
            createDirectory(directory)

            if iswebStatusOk(webpage):
                #get robots.txt files
                robotstxt = website + '/robots.txt'
                robotpage = requests.get(robotstxt, timeout=5) #attempt to download robots.txt and load response

                if iswebStatusOk(robotpage):
                    soup = BeautifulSoup(robotpage.content, 'html.parser')
                    filename = filepath + "\\robots.txt"
                    permission = "w"
                    writeFile(soup, filename, permission)
                else:
                    print("Unable to load robots.txt")

                #get html from website & store it in a file
                soup = BeautifulSoup(webpage.content, 'html.parser')
                filename = filepath + "\\" + websiteName + ".html"
                permission = "w"
                writeFile(soup, filename, permission)

                #get links from website & store it in a file
                filename = filepath + "\\links.txt"
                permission = "a+"
                data = webpage.text
                soup = BeautifulSoup(data, "lxml")
                for link in soup.find_all('a'):
                    writeFile(link.get('href'), filename, permission)
                    writeFile("\n", filename, permission)

                #get img tags from website & store it in a file
                filename = filepath + "\\images.txt"
                permission = "a+"
                data = webpage.text
                soup = BeautifulSoup(data, "lxml")
                #for image in soup.find_all("img")
                    #image = image.get('src')
                #print(image)

                print("Successfully downloaded " + website)
            else:
                print('Unable to download ' + website + ' with error code ' + webpage.status_code)
        except:
            print("Unable to download " + website)
            pass

        i += 1
#print(webpage.content)

main()
