import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

from src.context import SEARXNG_URL, PROXY, TOP_NUM, HEADERS
from src.utils import request_retry_with_backoff
from src.exceptions import MaxRetryRequestException, SearchException

class SearxngSpider:
    def __init__(self, categories: str = "general", language: str = "all", engines: str = "google,bing,yahoo", pageno: int = 1):
        self.categories = categories
        self.language = language
        self.engines = engines
        self.pageno = pageno
    
    def get_payload(self, domain: str) -> Dict[str, str]:
        return {
            "q": f"2FA%20OR%20MFA%20%22{domain}%22",
            "categories": self.categories,
            "language": self.language,
            "engines": self.engines,
            "pageno": self.pageno
        }

    def fetch_search_requests(self, data: Dict[str, str]) -> requests.Response:
        response = requests.post(url=SEARXNG_URL, data=data, proxies=PROXY, timeout=10, headers=HEADERS)
        response.raise_for_status()
        return response
    
    def parse_search_results(self, response: requests.Response) -> List[Dict[str, Optional[str]]]:
        soup = BeautifulSoup(response.text, 'html.parser')
        urls_element = soup.find(id='urls')

        if not urls_element:
            raise SearchException('No urls element found')
        
        articles = urls_element.find_all('article')
        if not articles:
            raise SearchException('No articles element found')

        return [self.extract_article_info(article) for article in articles[:TOP_NUM]]
    
    @request_retry_with_backoff(max_retries=3, initial_retry_interval=1)
    def search_domain_2fa(self, domain: str) -> List[Dict[str, Optional[str]]]:
        data = self.get_payload(domain)
        response = self.fetch_search_requests(data)
        return self.parse_search_results(response)  # assuming top_num is 10 for default

    def search(self, domain: str) -> List[Dict[str, Optional[str]]]:
        return self.search_domain_2fa(domain)

    def extract_article_info(self, article) -> Dict[str, Optional[str]]:
        return {
            "href": self.extract_href(article),
            "title": self.extract_text(article, 'h3'),
            "content": self.extract_text(article, 'p', 'content'),
            "engines": self.extract_engines(article)
        }

    @staticmethod
    def extract_href(article) -> Optional[str]:
        a_element = article.find('a', class_='url_wrapper')
        return a_element['href'] if a_element else None
    
    @staticmethod
    def extract_text(article, tag: str, class_: Optional[str] = None) -> Optional[str]:
        element = article.find(tag, class_=class_) if class_ else article.find(tag)
        return element.get_text(strip=True) if element else None
    
    @staticmethod
    def extract_engines(article) -> List[str]:
        div_element = article.find('div', class_='engines')
        return [span.get_text(strip=True) for span in div_element.find_all('span')] if div_element else []

