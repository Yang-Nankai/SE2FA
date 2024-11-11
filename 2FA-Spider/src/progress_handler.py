"""This module manages the program progress, allowing it to resume from the last checkpoint if paused or stopped."""

import os
import json
from typing import List
from src.context import PROGRESS_FILE


class ProgressHandler:
    """
    Handles the storage and retrieval of program progress.

    The progress is stored in a JSON file with the following structure:

    {
        "last_rank": 100,
        "error_ranks": [4, 16, 28, 45, 67],
        "error_reason": "File not found"
    }
    """

    def __init__(self, progress_file: str = PROGRESS_FILE) -> None:
        self.progress_file = progress_file
        self.progress = self._load_progress()

    def _load_progress(self) -> dict:
        if os.path.exists(self.progress_file):
            print("[INF] Found the progress file!")
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("[INF] Progress file not found. Starting fresh...")
            return {}

    def is_exists_progress(self) -> bool:
        return bool(self.progress)

    @property
    def last_rank(self) -> int:
        return self.progress.get('last_rank', 1)

    @property
    def error_ranks(self) -> List[int]:
        return self.progress.get('error_ranks', [])

    @property
    def error_reason(self) -> str:
        return self.progress.get('error_reason', '')

    def store_progress(self, last_rank: int, error_ranks: List[int], error_reason: str) -> None:
        self.progress = {
            "last_rank": last_rank,
            "error_ranks": error_ranks,
            "error_reason": error_reason
        }
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f)
