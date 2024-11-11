"""Global variables"""

import os
import random

SRC_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(SRC_PATH, '..')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
TESTS_PATH = os.path.join(PROJECT_ROOT, 'tests')

ASSETS_PATH = os.path.join(PROJECT_ROOT, 'assets')
DRIVER_PATH = os.path.join(ASSETS_PATH, 'driver')
FIREFOX_DRIVER_PATH = os.path.join(DRIVER_PATH, 'geckodriver.exe')
CHROME_DRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')
EDGE_DRIVER_PATH = os.path.join(DRIVER_PATH, 'edgedriver.exe')



TOP_WEBSITES_CSV_PATH = os.path.join(DATA_PATH, '10000-top-website.csv')
PROGRESS_FILE = os.path.join(DATA_PATH, 'progress.json')
RESULTS_FILE_PATH = os.path.join(DATA_PATH, 'searxng-result.csv')
RESULTS_JSON_PATH = os.path.join(DATA_PATH, 'searxng-result.json')

SEARXNG_URL = "https://searx.bndkt.io/search"

TOP_NUM = 5 # The top search results


PROXY = {
    "http" : "http://127.0.0.1:15732",
    "https" : "http://127.0.0.1:15732"
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
]

HEADERS = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}