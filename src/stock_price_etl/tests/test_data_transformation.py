import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from services.data_transformation import data_transformation, transformation

class TestDataTransformation(unittest.TestCase):

    @patch("services.data_transformation.sync_launcher")
    def test_data_transformation(self, mock_sync_launcher):
        mock_sync_launcher.return_value = None
        data_transformation()
        mock_sync_launcher.assert_called()

    @patch("services.data_transformation.load_json_data")
    @patch("services.data_transformation.save_csv_files")
    def test_transformation(self, mock_save_csv, mock_load_json):
        mock_load_json.return_value = {"mock_key": "mock_value"}
        transformation("AAPL")
        mock_load_json.assert_called()
        mock_save_csv.assert_called()
