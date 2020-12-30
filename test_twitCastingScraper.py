import unittest
import twitCastingScraper
from bs4 import BeautifulSoup
import csv
import requests
import sys
import os

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.req = requests.get("https://twitcasting.tv/natsuiromatsuri/show/")
        self.soup = BeautifulSoup(self.req.text, "html.parser")

    def test_soupSetup(self):
        self.assertEqual(self.req.status_code, 200)
        self.assertTrue(self.soup)

    # def test_linkCleanUp(self):
    # def test_updateLink(self):
    # def test_getDirectory(self):
    # def test_getFileName(self):
    # def test_checkFile(self):
    # def test_urlCount(self):
    # def test_linkScrape(self):
    # def test_scrapeChannel(self):


if __name__ == '__main__':
    unittest.main()
