
import os
from unittest import TestCase

from src.context import DATA_PATH
from src.result_handler import ResultHandler
from src.searxng_spider import SearxngSpider

class TestResultHandler(TestCase):
    def setUp(self) -> None:
        self.test_result_path = os.path.join(DATA_PATH, "test_searxng-results.csv")
        self.result_handler = ResultHandler(self.test_result_path)
        self.searxng_spider = SearxngSpider()

    def test_write_and_read(self):
        rank = 0
        domain = "google.com"
        matches = self.searxng_spider.search(domain)
        self.result_handler.write_matches(domain, rank, matches)
        
        # read
        matches = self.result_handler.read_matches()
        print(matches)

    def tearDown(self) -> None:
        self.result_handler.close()
        if os.path.exists(self.test_result_path):
            os.remove(self.test_result_path)