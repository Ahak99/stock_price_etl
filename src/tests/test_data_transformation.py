import unittest
from unittest.mock import patch
from src.services.data_transformation import transformation, data_transformation

class TestDataTransformation(unittest.TestCase):
    @patch("src.services.data_transformation.save_csv_files")
    @patch("src.services.data_transformation.load_json_data")
    @patch("src.services.data_transformation.get_latest_file")
    def test_transformation(self, mock_get_latest_file, mock_load_json_data, mock_save_csv_files):
        ticker = "AAPL"
        mock_get_latest_file.return_value = "s3://example.json"
        mock_load_json_data.return_value = {"key": "value"}

        transformation(ticker)

        mock_get_latest_file.assert_called_once_with(
            "s3://stocks-etl-bucket/raw_data/AAPL/AAPL_Company_Profile/AAPL_company_profile_*.json"
        )
        mock_load_json_data.assert_called_once_with("s3://example.json")
        mock_save_csv_files.assert_called_once_with(ticker, {"key": "value"})

    @patch("src.services.data_transformation.sync_launcher")
    @patch("src.services.data_transformation.get_sp500_constituents")
    def test_data_transformation(self, mock_get_sp500_constituents, mock_sync_launcher):
        mock_get_sp500_constituents.return_value = (
            ["AAPL", "MSFT"],
            {"Information Technology"},
            {"Information Technology": ["AAPL", "MSFT"]},
        )
        data_transformation()

        # Modify the args_list to only include tickers
        args_list = ["AAPL", "MSFT"]  # Only tickers, no tuple with unittest.mock.ANY
        mock_sync_launcher.assert_called_once_with(transformation, args_list)

if __name__ == "__main__":
    unittest.main()
