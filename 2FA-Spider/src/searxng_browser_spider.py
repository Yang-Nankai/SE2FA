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


# Assuming these constants are defined in a context file
from src.context import (FIREFOX_DRIVER_PATH, 
                     CHROME_DRIVER_PATH,
                     EDGE_DRIVER_PATH,
                     TOP_NUM, SEARXNG_URL)
from src.exceptions import SearchException
from src.browser_type import BrowserType

class SearxngBrowserSpider:
    def __init__(self, browser_type: int = BrowserType.CHROME.value) -> None:
        self.browser_type = browser_type
        self.driver = None
        self.service = None
        self.initialize_driver()
        # TODO: Need to add the cookie to set engines and language and other preferences

    def initialize_driver(self) -> None:
        """Initialize the webdriver based on the specified browser type."""
        if self.browser_type == BrowserType.FIREFOX.value:
            self.service = FirefoxService(FIREFOX_DRIVER_PATH)
            self.driver = webdriver.Firefox(service=self.service)
        elif self.browser_type == BrowserType.EDGE.value:
            self.service = EdgeService(EDGE_DRIVER_PATH)
            self.driver = webdriver.Edge(service=self.service)
        else:
            self.service = ChromeService(CHROME_DRIVER_PATH)
            self.driver = webdriver.Chrome(service=self.service)
        self.open_searxng()

    @property
    def browser_driver(self) -> webdriver:
        if not self.driver:
            self.initialize_driver()
        return self.driver

    def open_searxng(self) -> None:
        """Open SearXNG search page."""
        self.browser_driver.get(SEARXNG_URL)
        search_area = self.driver.find_element(By.XPATH, '//*[@id="q"]')
        search_area.clear()
        search_area.send_keys('2FA Test')
        search_area.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'results'))
        )

    def wait_for_page_load(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def extract_article_info(self, article: WebElement) -> Dict[str, Optional[str]]:
        return {
            "href": self.extract_href(article),
            "title": self.extract_text(article, 'h3'),
            "content": self.extract_text(article, 'p', 'content'),
            "engines": self.extract_engines(article)
        }

    @staticmethod
    def extract_href(article: WebElement) -> Optional[str]:
        try:
            a_element = article.find_element(By.CLASS_NAME, 'url_wrapper')
            return a_element.get_attribute('href')
        except NoSuchElementException:
            return None

    @staticmethod
    def extract_text(article: WebElement, tag: str, class_: Optional[str] = None) -> Optional[str]:
        try:
            if class_:
                # element = article.find_element(By.TAG_NAME, tag).find_element(By.CLASS_NAME, class_)
                # Fix the bug
                element = article.find_element(By.CLASS_NAME, class_)
            else:
                element = article.find_element(By.TAG_NAME, tag)
            return element.text.strip()
        except NoSuchElementException:
            return None

    @staticmethod
    def extract_engines(article: WebElement) -> List[str]:
        try:
            div_element = article.find_element(By.CLASS_NAME, 'engines')
            spans = div_element.find_elements(By.TAG_NAME, 'span')
            return [span.text.strip() for span in spans]
        except NoSuchElementException:
            return []

    def fetch_search_queries(self, domain: str) -> None:
        search_area = self.driver.find_element(By.XPATH, '//*[@id="q"]')
        search_area.clear()
        search_area.send_keys(f'2FA OR MFA "{domain}"')
        search_area.send_keys(Keys.RETURN)
        self.wait_for_page_load(10)

    def parse_search_results(self) -> List[Dict[str, Optional[str]]]:
        try:
            urls_element = self.driver.find_element(By.ID, 'urls')
            articles = urls_element.find_elements(By.TAG_NAME, 'article')
            return [self.extract_article_info(article) for article in articles[:TOP_NUM]]
        except NoSuchElementException:
            raise SearchException('No urls element found')

    def search_domain_2fa(self, domain: str) -> List[Dict[str, Optional[str]]]:
        """Perform search for 2FA OR MFA for the given domain."""
        self.fetch_search_queries(domain)
        return self.parse_search_results()

    def search(self, domain: str) -> List[Dict[str, Optional[str]]]:
        return self.search_domain_2fa(domain)

    def __del__(self) -> None:
        if self.driver:
            self.driver.quit()
