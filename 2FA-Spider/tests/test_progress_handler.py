import unittest
from unittest.mock import mock_open, patch
import os
import json

from src.progress_handler import ProgressHandler
from src.context import DATA_PATH

class TestProgressHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.progress_path = os.path.join(DATA_PATH, 'test_progress.json')
        test_progress = {"last_rank": 1, "error_ranks": [], "error_reason": "payload() missing 1 required positional argument: 'domain'"}
        with open(self.progress_path, 'w', encoding='utf-8') as f:
            json.dump(test_progress, f)

    def tearDown(self) -> None:
        if os.path.exists(self.progress_path):
            os.remove(self.progress_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"last_rank": 100, "error_ranks": [4, 16, 28, 45, 67], "error_reason": "File not found"}')
    def test_init_with_existing_file(self, mock_open, mock_exists):
        mock_exists.return_value = True
        
        handler = ProgressHandler(self.progress_path)
        
        self.assertTrue(mock_open.called)
        self.assertEqual(handler.progress['last_rank'], 100)
        self.assertEqual(handler.progress['error_ranks'], [4, 16, 28, 45, 67])
        self.assertEqual(handler.progress['error_reason'], "File not found")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_without_existing_file(self, mock_open, mock_exists):
        mock_exists.return_value = False
        
        handler = ProgressHandler(self.progress_path)
        
        self.assertFalse(mock_open.called)
        self.assertEqual(handler.progress, {})

    @patch('os.path.exists')
    def test_is_exists_progress(self, mock_exists):
        mock_exists.return_value = True
        handler = ProgressHandler(self.progress_path)
        
        handler.progress = {"last_rank": 100}
        self.assertTrue(handler.is_exists_progress())
        
        handler.progress = {}
        self.assertFalse(handler.is_exists_progress())

    @patch('os.path.exists')
    def test_last_rank(self, mock_exists):
        mock_exists.return_value = True
        handler = ProgressHandler(self.progress_path)
        
        handler.progress = {"last_rank": 100}
        self.assertEqual(handler.last_rank, 100)
        
        handler.progress = {}
        self.assertEqual(handler.last_rank, 1)

    @patch('os.path.exists')
    def test_error_ranks(self, mock_exists):
        mock_exists.return_value = True
        handler = ProgressHandler(self.progress_path)
        
        handler.progress = {"error_ranks": [1, 2, 3]}
        self.assertEqual(handler.error_ranks, [1, 2, 3])
        
        handler.progress = {}
        self.assertEqual(handler.error_ranks, [])

    @patch('os.path.exists')
    def test_error_reason(self, mock_exists):
        mock_exists.return_value = True
        handler = ProgressHandler(self.progress_path)
        
        handler.progress = {"error_reason": "some error"}
        self.assertEqual(handler.error_reason, "some error")
        
        handler.progress = {}
        self.assertEqual(handler.error_reason, "")

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_store_progress(self, mock_open, mock_exists):
        handler = ProgressHandler(self.progress_path)
        
        handler.store_progress(200, [10, 20, 30], "New error")
        
        expected_data = {
            "last_rank": 200,
            "error_ranks": [10, 20, 30],
            "error_reason": "New error"
        }
        
        self.assertEqual(handler.progress, expected_data)

if __name__ == '__main__':
    unittest.main()
