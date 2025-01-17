import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from services.data_extraction import data_extraction

class TestDataExtraction(unittest.TestCase):

    @patch("services.data_extraction.sync_launcher")
    def test_data_extraction(self, mock_sync_launcher):
        mock_sync_launcher.return_value = None
        data_extraction()
        mock_sync_launcher.assert_called()
