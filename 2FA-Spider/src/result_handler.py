import os
import csv
from typing import Optional, List, Dict, Tuple, Any


class ResultHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.csv_writer: Optional[csv.DictWriter] = None
        self.file_handler: Optional[object] = None

        if not os.path.exists(self.file_path):
            print(f"[INF] Result file does not exist, creating {self.file_path}")
            with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['domain', 'rank', 'no', 'href', 'title', 'content', 'engines'])
                writer.writeheader()

    @property
    def writer(self) -> csv.DictWriter:
        if self.csv_writer is None:
            self.file_handler = open(self.file_path, 'a', encoding='utf-8', newline='')
            self.csv_writer = csv.DictWriter(self.file_handler, fieldnames=['domain', 'rank', 'no', 'href', 'title', 'content', 'engines'])
        return self.csv_writer

    def read_matches(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Can't find the result file: {self.file_path}.")
        
        with open(self.file_path, 'r', encoding='utf-8', newline='') as file_handler:
            reader = csv.DictReader(file_handler)
            return [row for row in reader]

    def write_match(self, match_data: Tuple[str, int, int, Dict[str, Any]]) -> None:
        domain, rank, no, match = match_data
        result = {
            "domain": domain,
            "rank": rank,
            "no": no,
            "href": match.get('href', ''),
            "title": match.get('title', ''),
            "content": match.get('content', ''),
            "engines": match.get('engines', '')
        }
        self.writer.writerow(result)

    def write_matches(self, domain: str, rank: int, matches: List[Dict[str, Any]]) -> None:
        for no, match in enumerate(matches, start=1):
            self.write_match((domain, rank, no, match))
        if self.file_handler:
            self.file_handler.flush()
        print(f"[INF] Successfully written!")

    def close(self) -> None:
        if self.file_handler:
            self.file_handler.flush()
            self.file_handler.close()
            self.file_handler = None

    def __del__(self) -> None:
        self.close()
