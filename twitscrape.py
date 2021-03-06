#!/usr/bin/env python3
from bs4 import BeautifulSoup
import csv
import requests
import sys
import os
import argparse


# Adds a link, name, and output argument
# Returns the arguments
def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link',
                        type=str,
                        metavar='',
                        help="The TwitCasting channel link to scrape and get the video links")

    parser.add_argument('-n', '--name',
                        type=str,
                        nargs='+',
                        metavar='',
                        help="Name of the csv file. If not specified a default name will be used.")

    parser.add_argument('-o', '--output',
                        type=str,
                        nargs='+',
                        help="The user's chosen absolute save path for the csv file")

    args = parser.parse_args()
    return args


# Set up the soup and return it while requiring a link as an argument
def soupSetup(cleanLink):
    try:
        url = cleanLink
    except Exception:
        sys.exit("Invalid URL")
    req = requests.get(url)
    bSoup = BeautifulSoup(req.text, "html.parser")
    return bSoup


# Takes -l argument and "sanitize" url
# Returns the "sanitized" url
def linkCleanUp(argLink):
    if(argLink is not None):
        url = argLink
    else:
        url = input("URL: ")
    #Take a look at this if statement back in master branch
    if("https://" not in url and "http://" not in url):
        url = "https://" + url
    if ("/showclips" in url):
        cleanLink = url.split("/showclips")[0]
        cleanLink = cleanLink + "/showclips/"
        filterType = "showclips"
        return cleanLink, filterType
    elif("/show" in url):
        cleanLink = url.split("/show")[0]
        cleanLink = cleanLink + "/show/"
        filterType = "show"
        return cleanLink, filterType
    elif("twitcasting.tv/" in url):
        if(url.rindex("/") == len(url) - 1):
            cleanLink = url + "show/"
            return cleanLink, "show"
        else:
            cleanLink = url + "/show/"
            return cleanLink, "show"
    else:
        sys.exit("Invalid Link")
    return cleanLink


# Function takes in two arguments: the base link and page number
# Returns a new link by contacting base link and page number
def updateLink(baseLink, pageNumber):
    baseLink = baseLink
    updatedLink = baseLink + str(pageNumber)
    return updatedLink


# Function takes in a directory path argument
# Returns user specified directory path, else a default path is provided
def getDirectory(argOutput):
    if(argOutput is not None):
        # if(" " in argOutput):
        #     directoryPath = " ".join(argOutput)
        # else:
        #     directoryPath = argOutput
        directoryPath = argOutput
    else:
        directoryPath = os.getcwd()
    return directoryPath


# Function takes in 3 arguments: soup, sanitized link, and user input file name
# Returns a proper filename for the csv file based on user input
def getFileName(soup, cleanLink, argName):
    #Add special character exception
    if(argName is not None):
        joinedName = argName
        # Does nothing
        # if(" " in argName):
        #     joinedName = "_".join(argName)
        if (".csv" not in joinedName and isinstance(joinedName, list)):
            fileName = joinedName.append(".csv")
        if(".csv" not in joinedName):
            fileName = joinedName + ".csv"
        else:
            fileName = joinedName
    else:
        channelName = soup.find(class_="tw-user-nav-name").text
        if ("/showclips" in cleanLink):
            fileName = channelName.strip() + "_showclips.csv"
            return fileName
        elif("/show" in cleanLink):
            fileName = channelName.strip() + "_shows.csv"
            return fileName
        else:
            fileName = channelName.strip() + "_urls.csv"
            return fileName
    fileName = "".join(fileName)
    return fileName


# Function takes in the file name and check if it exists
# If the file exists, then remove it(replace the file)
def checkFile(fileName):
    if(os.path.isfile(fileName)):
        os.remove(fileName)


# Function that takes in two arguments: soup, and a filter of "show" or "showclips"
# Find the total page and gets the total link available to be scraped
# Returns a list that holds the total pages and total url available to be scraped
def urlCount(soup, filter):
    pagingClass = soup.find(class_="paging")
    pagingChildren = pagingClass.findChildren()
    totalPages = pagingChildren[len(pagingChildren)-1].text
    print("Total Pages: " + totalPages)

    if("showclips" in filter):
        btnFilter = soup.find_all("a", class_="btn")
        clipFilter = btnFilter[1]
        clipBtn = clipFilter.text
        totalUrl = clipBtn.replace("Clip ", "").replace("(", "").replace(")", "")
        print(totalUrl)
        return [totalPages, totalUrl]
    else:
        countLive = soup.find(class_="tw-user-nav-list-count")
        totalUrl = countLive.text
        print("Total Links: " + totalUrl)
        return [totalPages, totalUrl]


# Function takes two arguments: the file name and soup
# Scrapes the video urls and write it into a csv file
# Returns the number of video url extracted for that page
def linkScrape(fileName, soup):
    domainName = "https://twitcasting.tv"
    linksExtracted = 0
    with open(fileName, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        url_list = soup.find_all("a", class_="tw-movie-thumbnail")
        print("Links: " + str(len(url_list)))
        for link in url_list:
            linksExtracted = linksExtracted + 1
            hrefLink = domainName + link["href"]
            print(hrefLink)
            csv_writer.writerow([hrefLink])
    return linksExtracted


# Function that scrapes the entire channel while printing out
# various information onto the console
def scrapeChannel():
    # Links extracted
    linksExtracted = 0
    # Get commandline arguments
    args = arguments()
    # Get the clean twitcast channel link
    linkCleanedUp = linkCleanUp(args.link)
    channelLink = linkCleanedUp[0]
    channelFilter = linkCleanedUp[1]
    # Set up beautifulsoup
    soup = soupSetup(channelLink)
    # Get the filename
    fileName = getFileName(soup, channelLink, args.name)
    # Get the directory path
    directoryPath = getDirectory(args.output)
    # Set the directory path
    try:
        if isinstance(directoryPath, list):
            os.chdir(os.path.abspath(directoryPath[0]))
        else:
            os.chdir(os.path.abspath(directoryPath))
    except Exception as e:
        # sys.exit("Error setting output directory")
        sys.exit(e)
    # Check if the file exist and if it does delete it
    checkFile(fileName)
    # Count the total pages and links to be scraped
    countList = urlCount(soup, channelFilter)
    totalPages = countList[0]
    totalLinks = countList[1]
    # Print file name
    print("Filename: " + fileName)
    for currentPage in range(int(totalPages)):
        if (currentPage == int(totalPages)):
            print("\nPage: " + str(currentPage - 1))
        else:
            print("\nPage: " + str(currentPage + 1))
        if (currentPage != 0):
            updatedLink = updateLink(channelLink, currentPage)
            soup = soupSetup(updatedLink)
        linksExtracted += linkScrape(fileName, soup)
    print("\nTotal Links Extracted: " + str(linksExtracted) + "/" + totalLinks + "\nExiting")


if __name__ == '__main__':
    scrapeChannel()