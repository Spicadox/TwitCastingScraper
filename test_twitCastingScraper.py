import unittest
from unittest.mock import patch
import twitCastingScraper
from bs4 import BeautifulSoup
import csv
import requests
import sys
import os
import pytest
import builtins

# class MyTestCase(unittest.TestCase):
#     def setUp(self):
#         self.req = requests.get("https://twitcasting.tv/natsuiromatsuri/show/")
#         self.soup = BeautifulSoup(self.req.text, "html.parser")
#
#     def test_soupSetup(self):
#         self.assertEqual(self.req.status_code, 200)
#         self.assertTrue(self.soup)
#
#         twitCastingScraper.soupSetup("https://twitcasting.tv/natsuiromatsuri/show/")
#         self.assertEqual(self.req.status_code, 200)
#         self.assertTrue(self.soup)
#
#     @patch("twitCastingScraper.linkCleanUp", create=True)
#     def test_linkCleanUp(self, mocked_input):
#         mocked_input.side_effect = ["https://twitcasting.tv/natsuiromatsuri/show/"]
#         link_tuple = twitCastingScraper.linkCleanUp()
#         link = link_tuple[0]
#         filter = link_tuple[1]
#         self.assertEqual(twitCastingScraper.linkCleanUp()[0], "https://twitcasting.tv/natsuiromatsuri/show/")
#         self.assertEqual(link, "https://twitcasting.tv/natsuiromatsuri/show/")
#         self.assertEqual(filter, "show")

    # def test_updateLink(self):
    # def test_getDirectory(self):
    # def test_getFileName(self):
    # def test_checkFile(self):
    # def test_urlCount(self):
    # def test_linkScrape(self):
    # def test_scrapeChannel(self):
class TestClass:

    def setUp(self):
        self.req = requests.get("https://twitcasting.tv/natsuiromatsuri/show/")
        self.soup = BeautifulSoup(self.req.text, "html.parser")


    def test_soupSetup(self):
        self.setUp()
        assert self.req.status_code == 200
        assert self.soup is not None

        twitCastingScraper.soupSetup("https://twitcasting.tv/natsuiromatsuri/show/")
        assert self.req.status_code == 200
        assert self.soup is not None

    def test_linkCleanUp(self):
        # monkeypatch.setattr('builtins.input', lambda _: "Mark")
        # builtins.input = lambda: "https://twitcasting.tv/natsuiromatsuri/show/"
        output = twitCastingScraper.linkCleanUp()
        link = output[0]
        filter = output[1]

        assert link == "https://twitcasting.tv/natsuiromatsuri/show/"
        assert filter == "show"
        # mocked_input.side_effect = ["https://twitcasting.tv/natsuiromatsuri/show/"]
        # link_tuple = twitCastingScraper.linkCleanUp()
        # link = link_tuple[0]
        # filter = link_tuple[1]
        # self.assertEqual(twitCastingScraper.linkCleanUp()[0], "https://twitcasting.tv/natsuiromatsuri/show/")
        # self.assertEqual(link, "https://twitcasting.tv/natsuiromatsuri/show/")
        # self.assertEqual(filter, "show")

if __name__ == '__main__':
    TestClass()
