#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by P. Renee Carnley for CSC 842 Green Team Cycle 11 #
# Scrapper is a simiple web scraping tool to gather web files #
# ****DISCLAIMER - author is not responsible for illegal use  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from bs4 import BeautifulSoup
import os
import pathlib
import random
import requests
import signal
import socket
import subprocess
import sys
import time
import threading
import urllib
import webbrowser

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

#write scrapped contents to file
def writeFile(content, file, permission):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, permission, encoding="utf-8") as f:
        f.write(str(content))

#read websites from file
def readFile(file):
    print("reading file " + file)
    array = []
    try:
        sites = open(file)
        for line in sites.read().split():
            array.append(line)
        return array
    except IOError:
        return "Error"

#scan ports
def knocker(website, timeout, randomizer, numports):
    #check for open ports
    try:
        #initialize variables for counting number of open and closed ports
        numOpen = 0
        numClosed = 0

        #initialize total possible numports
        totalports = 65535
        server = socket.gethostbyname(website) #get the IP address of the website

        print ('knocking on ' + website + ' at ip: ' + server)
        #knock on ports
        for i in range(1, numports):
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(timeout)

            if randomizer == "n":
                port = i;
            else:
                #randomly get a port number within range
                port = random.randint(1,totalports)

            knock = soc.connect_ex((server, port))
            print ("Port {}: ".format(port), end="")

            #check if port is opened
            if knock == 0:
                print ("open")
                numOpen += 1
            else:
                print ("closed")
                numClosed += 1
            soc.close()

    #catch if bad website name
    except socket.gaierror:
        print ('Website name failed ')
        sys.exit()

    #catch if no connection to website could be made
    except socket.error:
        print ('Could not connect to website')
        sys.exit()

    #catch if connection timed out
    except socket.timeout:
        print ('Connection timed out')

    #catch if user wants to stop
    except KeyboardInterrupt:
        print('User Interrupt....shutting down')
        soc.close() #ensure socket is closed before exiting
        sys.exit()

    print ('Number of open ports {} Number of closed ports {}'.format(numOpen, numClosed))

def main():
    sitefile = input("\nEnter the path and name of the URL file: \n") #get file path
    websites = readFile(sitefile) #set array websites to the user defined ones from given file

    #Check if valid file was found. If not ask for another
    if (websites == "Error"):
        sitefile = input("\nFile not found. Please enter the path and name of another file \n")
        websites = readFile(sitefile)

    userpath = input("\nEnter the path and name of directory where you want the scrapped files stored: \n")

    toknock = input("\nDo you wish to port scan the websites y/n\n")
    if(toknock == "y"):
       print("\nDo you wish to use default settings?")
       default = input("\nRandomizer is off, Socket time out is 3 seconds, and number of ports is 65536? y/n\n")
       if(default == "y"):
           timeout = 3
           random = "n"
           ports = 65536
       else:
           timeout = int(input("\nEnter the number of seconds till socket timeout: "))
           random = input("\nTurn randomizer on? y/n")
           ports = int(input("\nEnter the number of ports to scan (1 thru 65536): "))

    i = 0
    while i < len(websites):
        try:
            website = str(websites[i])
            webpage = requests.get(website, timeout=5) #attempt to download website & load response

            tempname = website.split(".") #break url into an array get name of website
            websiteName = tempname[1] + "." + tempname[2] #get the name of website
            filepath = userpath + '\\' + websiteName #set filepath name with website name
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

                print("\nSuccessfully downloaded " + website + " in directory " + filepath)

                knocker(websiteName, timeout, random, ports)

            else:
                print('Unable to download ' + website + ' with error code ' + webpage.status_code)
        except:
            print("Unable to complete " + website)
            pass




        i += 1
#print(webpage.content)

main()
