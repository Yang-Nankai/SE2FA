import os
import time
import random
import pandas as pd
from typing import Dict, List

from src.searxng_spider import SearxngSpider
from src.searxng_browser_spider import SearxngBrowserSpider
from src.progress_handler import ProgressHandler
from src.result_handler import ResultHandler
from src.exceptions import MaxRetryRequestException, SearchException
from src.context import RESULTS_FILE_PATH

class Search:
    pass

class SearxngSearch(Search):

    def __init__(self, domains_file: str) -> None:
        super().__init__()
        if not os.path.exists(domains_file):
            raise FileNotFoundError(f"Can't find the domains file: {domains_file}.")
        
        _, extension = os.path.splitext(domains_file)

        if not extension.lower() == '.csv':
            raise ValueError("The domain file must be a CSV file.")
        
        self.domains_file = domains_file
        self.error_ranks: List[int] = []

    @property
    def domain_pairs(self) -> Dict[str, str]:
        try:
            data = pd.read_csv(self.domains_file)
            return dict(zip(data.iloc[:, 0], data.iloc[:, 1]))
        except Exception as e:
            print(f"\033[91m[ERR] Failed to read the domain CSV file: {e}\033[0m")
            return {}

    def get_domain_pairs(self, start: int, end: int, error_ranks: List[int]) -> Dict[int, str]:
        domain_pairs = self.domain_pairs
        now_domain_pairs = {rank: domain_pairs[rank] for rank in range(start, end + 1) if rank in domain_pairs}
        now_domain_pairs.update({rank: domain_pairs[rank] for rank in error_ranks if rank in domain_pairs.keys() and rank <= end})
        return now_domain_pairs

    def run(self, end: int = 1):
        progress = ProgressHandler()

        start = end + 1 if progress.last_rank > end + 1 else progress.last_rank
        current = start

        domains_pairs = self.get_domain_pairs(start, end, progress.error_ranks)

        # TODO: assign to Xin, change error_ranks to default class param
        self.error_ranks.extend(progress.error_ranks)

        # TODO: We can switch to selenium or requests
        # searxng_spider = SearxngSpider()
        searxng_spider = SearxngBrowserSpider()
        result_handler = ResultHandler(RESULTS_FILE_PATH)

        for rank, domain in domains_pairs.items():
            try:
                print(f"[INF] Searching for {rank} - {domain}")
                
                # TODO: Just for test sleep
                time.sleep(random.uniform(1, 5))
                
                matches = searxng_spider.search(domain)
                result_handler.write_matches(domain, rank, matches)
                print(f"\033[92m[SUS] Successfully searched for {rank} - {domain}\033[0m")
                current = rank

                # TODO: assign to Xin, change error_ranks to default class param
                if current in self.error_ranks:
                    self.error_ranks.remove(current)

            except MaxRetryRequestException as e:
                print(f"\033[91m[ERR] Failed to search {domain}, reason: {e}\033[0m")
                self.error_ranks.append(rank)
            finally:
                # Save progress after each domain to avoid losing data in case of failure
                last_rank = current if current > progress.last_rank else progress.last_rank
                progress.store_progress(last_rank, self.error_ranks, error_reason="")

        # Save final progress in case of a successful run
        last_rank = current + 1 if current + 1 > progress.last_rank else progress.last_rank
        progress.store_progress(last_rank, self.error_ranks, error_reason="")

