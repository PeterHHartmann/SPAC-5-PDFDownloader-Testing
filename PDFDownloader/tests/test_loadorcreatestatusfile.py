import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from pdf_downloader.downloader import load_or_create_status_file

class TestLoadOrCreateStatusFile(unittest.TestCase):
    @patch("os.path.isfile", return_value=False)
    @patch("logging.getLogger")
    def test_file_does_not_exist(self, mock_logger, mock_isfile):
        logger_instance = MagicMock()
        mock_logger.return_value = logger_instance
        
        df = load_or_create_status_file("nonexistent.xlsx")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["BRnum", "Status", "Info"])
        logger_instance.info.assert_called_with("Status file not found. Creating: nonexistent.xlsx")

    @patch("os.path.isfile", return_value=True)
    @patch("pandas.read_excel", return_value=pd.DataFrame(columns=["BRnum", "Status", "Info"]))
    @patch("logging.getLogger")
    def test_file_exists_with_correct_columns(self, mock_logger, mock_read_excel, mock_isfile):
        df = load_or_create_status_file("existing.xlsx")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["BRnum", "Status", "Info"])
        mock_read_excel.assert_called_once_with("existing.xlsx")

    @patch("os.path.isfile", return_value=True)
    @patch("pandas.read_excel", return_value=pd.DataFrame(columns=["BRnum", "WrongColumn"]))
    @patch("logging.getLogger")
    def test_file_exists_with_missing_columns(self, mock_logger, mock_read_excel, mock_isfile):
        logger_instance = MagicMock()
        mock_logger.return_value = logger_instance
        
        df = load_or_create_status_file("missing_columns.xlsx")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["BRnum", "Status", "Info"])
        logger_instance.warning.assert_called_with("Status file missing columns. Recreating.")

    @patch("os.path.isfile", return_value=True)
    @patch("pandas.read_excel", side_effect=Exception("Read error"))
    @patch("logging.getLogger")
    def test_file_read_failure(self, mock_logger, mock_read_excel, mock_isfile):
        logger_instance = MagicMock()
        mock_logger.return_value = logger_instance
        
        df = load_or_create_status_file("corrupt.xlsx")
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["BRnum", "Status", "Info"])
        logger_instance.fatal.assert_called_with("Failed to read status file corrupt.xlsx: Read error")

if __name__ == "__main__":
    unittest.main()
