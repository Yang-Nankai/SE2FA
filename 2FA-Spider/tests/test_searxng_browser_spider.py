import unittest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import List, Dict, Optional

from src.context import FIREFOX_DRIVER_PATH, CHROME_DRIVER_PATH, EDGE_DRIVER_PATH, TOP_NUM, SEARXNG_URL
from src.exceptions import SearchException
from src.browser_type import BrowserType
from src.searxng_browser_spider import SearxngBrowserSpider  # Import the class to be tested

class TestSearxngBrowserSpider(unittest.TestCase):
    @patch('selenium.webdriver.Firefox')
    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.Edge')
    def setUp(self, MockEdge, MockChrome, MockFirefox) -> None:
        self.mock_chrome = MockChrome
        self.mock_firefox = MockFirefox
        self.mock_edge = MockEdge
        self.driver_mock = MagicMock()
        self.mock_chrome.return_value = self.driver_mock
        self.mock_firefox.return_value = self.driver_mock
        self.mock_edge.return_value = self.driver_mock

    def test_initialize_driver_chrome(self):
        spider = SearxngBrowserSpider(browser_type=BrowserType.CHROME.value)
        self.assertIsInstance(spider.driver, webdriver.Chrome)

    def test_initialize_driver_firefox(self):
        spider = SearxngBrowserSpider(browser_type=BrowserType.FIREFOX.value)
        self.assertIsInstance(spider.driver, webdriver.Firefox)

    def test_initialize_driver_edge(self):
        spider = SearxngBrowserSpider(browser_type=BrowserType.EDGE.value)
        self.assertIsInstance(spider.driver, webdriver.Edge)

    def test_search_domain_2fa(self):
        spider = SearxngBrowserSpider()
        spider.fetch_search_queries = MagicMock()
        spider.parse_search_results = MagicMock(return_value=[{'href': 'http://test.com'}])
        results = spider.search_domain_2fa('example.com')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['href'], 'http://test.com')

    def tearDown(self) -> None:
        if hasattr(self, 'spider'):
            self.spider.__del__()

if __name__ == '__main__':
    unittest.main()
