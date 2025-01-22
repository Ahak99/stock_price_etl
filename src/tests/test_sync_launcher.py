import unittest
from unittest.mock import patch
from src.services.sync_launcher import sync_launcher

class TestSyncLauncher(unittest.TestCase):
    @patch("multiprocessing.Pool")
    def test_sync_launcher_with_tuples(self, mock_pool):
        args_list = [(1, 2), (3, 4)]
        sync_launcher(lambda x, y: x + y, args_list)
        mock_pool.assert_called_once()

    @patch("multiprocessing.Pool")
    def test_sync_launcher_with_single_arg(self, mock_pool):
        args_list = [1, 2, 3, 4]
        sync_launcher(lambda x: x + 1, args_list)
        mock_pool.assert_called_once()

if __name__ == "__main__":
    unittest.main()