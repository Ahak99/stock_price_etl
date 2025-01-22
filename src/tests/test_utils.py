import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import unittest
from unittest import mock
from unittest.mock import patch, mock_open
from utils import (
    get_sp500_constituents, get_latest_file, load_json_data, append_to_csv, normalize_value
)

class TestUtils(unittest.TestCase):

    @patch('utils.pd.read_html')
    def test_get_sp500_constituents(self, mock_read_html):
        # Mock a DataFrame that matches the structure expected in get_sp500_constituents
        mock_df = pd.DataFrame({
            'Symbol': ['AAPL'],
            'GICS Sector': ['Information Technology']
        })
        mock_read_html.return_value = [mock_df]  # pd.read_html returns a list of DataFrames

        # Call the function
        tickers, sectors, tickers_sector = get_sp500_constituents()

        # Assert the results
        self.assertEqual(tickers, ['^GSPC', 'AAPL'])  # ^GSPC is prepended
        self.assertEqual(sectors, {'Information Technology'})
        self.assertEqual(tickers_sector['Information Technology'], ['AAPL'])

    @patch('utils.s3fs.S3FileSystem')
    def test_get_latest_file(self, mock_s3):
        mock_s3.return_value.glob.return_value = ['file1', 'file2']
        mock_s3.return_value.info.side_effect = lambda x: {'LastModified': '2025-01-01'} if x == 'file2' else {'LastModified': '2024-01-01'}
        latest_file = get_latest_file("s3://path/*.json")
        self.assertEqual(latest_file, 'file2')
    
    @patch('utils.s3fs.S3FileSystem')
    def test_load_json_data(self, mock_s3):
        mock_s3.return_value.open = mock_open(read_data='{"key": "value"}')
        data = load_json_data("s3://path/file.json")
        self.assertEqual(data, {"key": "value"})

    @patch('utils.pd.DataFrame.to_csv')
    @patch('utils.s3fs.S3FileSystem')
    def test_append_to_csv(self, mock_s3, mock_to_csv):
        data_dict = {"col": "value"}
        append_to_csv(data_dict, "s3://path/file.csv")
        mock_to_csv.assert_called_once()

    def test_normalize_value(self):
        self.assertEqual(normalize_value("10%"), 0.1)
        self.assertEqual(normalize_value("1.5B"), 1.5e9)
        self.assertTrue(pd.isna(normalize_value("random")))
