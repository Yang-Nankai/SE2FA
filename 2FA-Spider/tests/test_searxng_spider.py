from unittest import TestCase
from src.searxng_spider import SearxngSpider

class TestSearxngSpider(TestCase):

    def setUp(self) -> None:
        self.searxng_spider = SearxngSpider()

    def test_get_payload(self):
        domain = 'google.com'
        payload = self.searxng_spider.get_payload(domain)
        test_payload = {
            "q": f"2FA%20OR%20MFA%20%22google.com%22",
            "categories": "general",
            "language": "all",
            "engines": "google,bing,yahoo",
            "pageno": 1
        }

        self.assertIsNotNone(payload)
        self.assertEqual(payload, test_payload)

    def test_fetch_search_requests(self):
        domain = 'google.com'
        payload = self.searxng_spider.get_payload(domain)

        self.assertIsNotNone(payload)

        response = self.searxng_spider.fetch_search_requests(payload)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)

    def test_search(self):
        domain = 'google.com'
        matches = self.searxng_spider.search(domain)

        self.assertGreater(len(matches), 0)
        self.assertIsNotNone(matches[0])
        self.assertIsNotNone(matches[0].get('href'))




    

        