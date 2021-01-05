# TwitCastingScraper
### Overview

A CLI script that grabs all video links from a TwitCasting channel. It can grab either videos from "shows" or "showclips".
An executable version of the script is provided where it request the TwitCasting channel link from the user.


### Installation

Requires the nonbinary library [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)

A requirements text file has been included and the command `pip3 install -r requirements.txt` (or pip) can be used to install BeautifulSoup.

Note: The installation of BeautifulSoup is not required for the executable file.


### Options and Usages
```
usage: twitscrape.py [-h] [-l] [-n  [...]] [-o OUTPUT [OUTPUT ...]]

optional arguments:
  -h, --help        show this help message and exit
  -l, --link        The TwitCasting channel link to scrape and get the video links
  -n, --name        Name of the csv file. If not specified a default name will be used.
  -o, --output      The user's chosen absolute save path for the csv file

 ```
 Examples: 
 
 `python twitscape.py -l <TwitCasting Link>`
 
 `python twitscape.py -l <TwitCasting Link> -n "output.csv" -o <Path>`
