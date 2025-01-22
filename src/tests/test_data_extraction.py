import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, call
from datetime import datetime
from services.data_extraction import extraction, data_extraction

class TestDataExtraction(unittest.TestCase):
    @patch("services.data_extraction.get_company_profile")
    def test_extraction(self, mock_get_company_profile):
        ticker = "AAPL"
        p_run_time = datetime.now()
        extraction(ticker, p_run_time)
        mock_get_company_profile.assert_called_once_with(ticker, p_run_time)

    @patch("services.data_extraction.sync_launcher")
    @patch("services.data_extraction.get_sp500_constituents")
    def test_data_extraction(self, mock_get_sp500_constituents, mock_sync_launcher):
        mock_get_sp500_constituents.return_value = (
            ["AAPL", "MSFT"],
            {"Information Technology"},
            {"Information Technology": ["AAPL", "MSFT"]},
        )
        data_extraction()
        args_list = [(ticker, unittest.mock.ANY) for ticker in ["AAPL", "MSFT"]]
        mock_sync_launcher.assert_called_once_with(unittest.mock.ANY, args_list)

if __name__ == "__main__":
    unittest.main()
