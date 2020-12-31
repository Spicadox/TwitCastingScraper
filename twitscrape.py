from bs4 import BeautifulSoup
import csv
import requests
import sys
import os
import argparse


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

def soupSetup(cleanLink):
    try:
        url = cleanLink
    except Exception:
        sys.exit("Invalid URL")
    req = requests.get(url)
    bSoup = BeautifulSoup(req.text, "html.parser")
    return bSoup


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


def updateLink(baseLink, pageNumber):
    baseLink = baseLink
    updatedLink = baseLink + str(pageNumber)
    return updatedLink


def getDirectory(argOutput):
    if(argOutput is not None):
        directoryPath = " ".join(argOutput)
    else:
        directoryPath = os.getcwd()
    return directoryPath


def getFileName(soup, cleanLink, argName):
    if(argName is not None):
        joinedName = "_".join(argName)
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
    return fileName


def checkFile(fileName):
    if(os.path.isfile(fileName)):
        os.remove(fileName)


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
    os.chdir(os.path.abspath(directoryPath))
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