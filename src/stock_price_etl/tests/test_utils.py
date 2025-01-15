import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open
from utils import (
    normalize_value,
    get_sp500_constituents,
    save_to_json,
    load_json_data,
    get_latest_file
)
import os
import pandas as pd

class TestUtils(unittest.TestCase):

    def test_normalize_value(self):
        self.assertEqual(normalize_value("10%"), 0.1)
        self.assertEqual(normalize_value("1.2B"), 1.2e9)
        self.assertEqual(normalize_value("500M"), 500e6)
        self.assertEqual(normalize_value("12K"), 12000)
        self.assertTrue(pd.isna(normalize_value("invalid")))
        self.assertTrue(pd.isna(normalize_value(None)))

    @patch("pandas.read_html")
    def test_get_sp500_constituents(self, mock_read_html):
        # Mock Wikipedia table
        mock_table = pd.DataFrame({
            "Symbol": ["AAPL", "MSFT", "GOOGL"],
            "GICS Sector": ["Information Technology", "Information Technology", "Communication Services"]
        })
        mock_read_html.return_value = [mock_table]

        tickers, sectors, tickers_sector = get_sp500_constituents()
        self.assertIn("^GSPC", tickers)
        self.assertEqual(tickers_sector["Information Technology"], ["AAPL", "MSFT"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_to_json(self, mock_makedirs, mock_open_file):
        data = {"key": "value"}
        save_to_json(data, "AAPL", "path/to/json", "data_type", "timestamp")
        mock_makedirs.assert_called_once_with("path/to/json", exist_ok=True)
        mock_open_file.assert_called_once_with("path/to/json/AAPL_data_type_timestamp.json", "w")

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_data(self, mock_open_file):
        result = load_json_data("path/to/json/file.json")
        self.assertEqual(result, {"key": "value"})
        mock_open_file.assert_called_once_with("path/to/json/file.json", "r")

    @patch("glob.glob")
    @patch("os.path.getmtime")
    def test_get_latest_file(self, mock_getmtime, mock_glob):
        mock_glob.return_value = ["file1.json", "file2.json"]
        mock_getmtime.side_effect = [1, 2]
        latest_file = get_latest_file("*.json")
        self.assertEqual(latest_file, "file2.json")
