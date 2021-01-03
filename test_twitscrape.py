import twitscrape
from bs4 import BeautifulSoup
import requests
import requests
from bs4 import BeautifulSoup
import pytest
import twitscrape
import os
from unittest.mock import patch
import csv
import sys

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

    def setUp(self, link):
        url = link
        self.req = requests.get(url)
        self.soup = BeautifulSoup(self.req.text, "html.parser")
        # if(sys.argv >= 2):

    def test_soupSetup(self):
        self.setUp("https://twitcasting.tv/natsuiromatsuri/show/")
        assert self.req.status_code == 200
        assert self.soup is not None

        twitscrape.soupSetup("https://twitcasting.tv/natsuiromatsuri/show/")
        assert self.req.status_code == 200
        assert self.soup is not None

    # Simulate argument input rather than system user input
    def test_linkCleanUp(self):
        #Test url with show filter
        working_url_list = ["https://twitcasting.tv/natsuiromatsuri/show/",
                            "https://twitcasting.tv/natsuiromatsuri/show", "https://twitcasting.tv/natsuiromatsuri/",
                            "https://twitcasting.tv/natsuiromatsuri", "twitcasting.tv/natsuiromatsuri/show/",
                            "twitcasting.tv/natsuiromatsuri/show", "twitcasting.tv/natsuiromatsuri/",
                            "twitcasting.tv/natsuiromatsuri", "twitcasting.tv/natsuiromatsuri"]
        for link in working_url_list:
            output = twitscrape.linkCleanUp(link)
            domain = output[0]
            filter = output[1]

            assert domain == "https://twitcasting.tv/natsuiromatsuri/show/"
            assert filter == "show"

        # Test url with showclips
        working_url_showclips_list = ["https://twitcasting.tv/natsuiromatsuri/showclips/",
                            "https://twitcasting.tv/natsuiromatsuri/showclips", "twitcasting.tv/natsuiromatsuri/showclips/",
                            "twitcasting.tv/natsuiromatsuri/showclips"]
        for link in working_url_showclips_list:
            output = twitscrape.linkCleanUp(link)
            domain = output[0]
            filter = output[1]
            assert domain == "https://twitcasting.tv/natsuiromatsuri/showclips/"
            assert filter == "showclips"
        # Test url with http protocol
        working_url_http_list = ["http://twitcasting.tv/natsuiromatsuri/show/",
                            "http://twitcasting.tv/natsuiromatsuri/show", "http://twitcasting.tv/natsuiromatsuri/",
                            "http://twitcasting.tv/natsuiromatsuri", "http://twitcasting.tv/natsuiromatsuri/showclips/",
                            "http://twitcasting.tv/natsuiromatsuri/showclips"]
        for link in working_url_http_list:
            output = twitscrape.linkCleanUp(link)
            domain = output[0]
            filter = output[1]
            if "showclips" in link:
                assert domain == "http://twitcasting.tv/natsuiromatsuri/showclips/"
                assert filter == "showclips"
            else:
                assert domain == "http://twitcasting.tv/natsuiromatsuri/show/"
                assert filter == "show"

        # Test invalid urls
        invalid_url_list = ["twitcasting.tv", "https://twitcasting.tv", "http://twitcasting.tv/natsuiromatsuri/show/", "youtube.com", "https://youtube.com", 15215215421, True, False]
        with pytest.raises(SystemExit):
            for link in invalid_url_list:
                twitscrape.linkCleanUp(link)
                assert "Invalid Link"


    def test_updateLink(self):
        # Test show tab pagination
        for page in range(17):
            updatedLink = twitscrape.updateLink("https://twitcasting.tv/natsuiromatsuri/show/", page)
            assert updatedLink == "https://twitcasting.tv/natsuiromatsuri/show/" + str(page)
        # Test showclips tab pagination
        for page in range(1):
            updatedLink = twitscrape.updateLink("https://twitcasting.tv/natsuiromatsuri/showclips/", page)
            assert updatedLink == "https://twitcasting.tv/natsuiromatsuri/showclips/" + str(page)

    def test_getDirectory(self):
        directory = [os.path.abspath("I:\\"), os.path.abspath("C:\\Program Files (x86)\\Temp"), os.path.abspath("C:\\Program Files  (x86)\\Temp"), os.path.abspath("C:\\Program Files   (x86)\\Temp"), os.path.abspath("C:\\Program Files&(x86)\\Temp"), " ", ""]
        #defaultPath = "C:\\Users\\samph\\PycharmProjects\\TwitCastingScraper"
        for location in directory:
            directoryPath = twitscrape.getDirectory(location)
            assert directoryPath == location

    def test_getFileName(self):
        self.setUp("https://twitcasting.tv/natsuiromatsuri/show/")
        # cleanLink = ["https://twitcasting.tv/natsuiromatsuri/showclips/", "https://twitcasting.tv/natsuiromatsuri/show/", "https://twitcasting.tv/natsuiromatsuri/"]
        cleanLink = "https://twitcasting.tv/natsuiromatsuri/"
        argNames = ["name", "$*(@$&", "my name", "yes.csv"]
        # expected_filename_list = ["name_showclips.csv", "name_show.csv", "name_urls.csv", "$*(@$&)_showclips.csv",
        #                           "$*(@$&)_show.csv", "$*(@$&)_urls.csv", "my_name_showclips.csv", "my_name_show.csv",
        #                           "my_name_urls.csv", "yes.csv", "yes.csv", "yes.csv"]
        expected_filename_list = ["name.csv", "$*(@$&.csv", "my name.csv", "yes.csv"]
        for i in range(len(argNames)):
            filename = twitscrape.getFileName(self.soup, cleanLink, argNames[i])
            assert filename == expected_filename_list[i]

    @patch("os.remove")
    @patch("os.path.isfile")
    def test_checkFile(self, mock_removed, mock_isfile):
        twitscrape.checkFile("testing.csv")
        assert mock_removed.called
        assert mock_isfile.called

    def test_urlCount(self):
        self.setUp("https://twitcasting.tv/natsuiromatsuri/show/")
        total_show_filter = twitscrape.urlCount(self.soup, "show")
        assert total_show_filter[0] == "17"
        assert total_show_filter[1] == "148"
        self.setUp("https://twitcasting.tv/natsuiromatsuri/showclips/")
        total_showclips_filter = twitscrape.urlCount(self.soup, "showclips")
        assert total_showclips_filter[0] == "1"
        assert total_showclips_filter[1] == "1"

    def test_linkscrape(self):
        self.setUp("https://twitcasting.tv/natsuiromatsuri/showclips/")
        linksExtracted = twitscrape.linkScrape("linkscrape_test.csv", self.soup)
        with open("linkscrape_test.csv", 'r') as test_file:
            csv_reader = csv.reader(test_file)
            for row in csv_reader:
                assert row[0] == "https://twitcasting.tv/clipview.php?movie_id=595762685&clip_id=35110"
        assert linksExtracted == 1
        os.remove("linkscrape_test.csv")

    def test_scrapeChannel(self):
        if(len(sys.argv) > 1):
            with pytest.raises(SystemExit):
                twitscrape.scrapeChannel()


if __name__ == '__main__':
    TestClass()
