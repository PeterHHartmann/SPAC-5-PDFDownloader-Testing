import os
import shutil
import unittest
from unittest.mock import patch

import pandas as pd
from pdf_downloader.downloader import download_single_pdf

class TestDownloadSinglePDF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = pd.read_excel(
            io="tests/test_data/GRI_sample.xlsx",
            sheet_name=0,
            engine="openpyxl"
        )
        cls.test_download_dir="tests/temp/PDFs"
        cls.test_status_file_dir = "tests/temp/DownloadedStatus.xlsx"

    def setUp(self):
        os.makedirs(self.test_download_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree("tests/temp")

    @patch("logging.getLogger")
    @patch("threading.current_thread")
    @patch("pdf_downloader.downloader.parse_thread_name_to_id", return_value=1)
    @patch("pdf_downloader.downloader._push_thread_update")
    def test_primary_url_success(
        self, mock_logger, mock_thread, mock_parse, mock_push,
    ):
        br_num = "BR50077"
        test_row = self.test_data[self.test_data["BRnum"] == br_num].iloc[0]

        result = download_single_pdf(
            brnum=test_row["BRnum"], 
            primary_url=test_row.get("Pdf_URL"), 
            secondary_url=test_row.get("Report Html Address"), 
            output_folder=self.test_download_dir
        )
        self.assertEqual(result, ("Success", "Primary link OK"))
        file_count = len(os.listdir(self.test_download_dir))
        self.assertEqual(file_count, 1)

    @patch("logging.getLogger")
    @patch("threading.current_thread")
    @patch("pdf_downloader.downloader.parse_thread_name_to_id", return_value=1)
    def test_secondary_url_success(
        self, mock_logger, mock_thread, mock_parse
    ):
        br_num = "BR50101"
        test_row = self.test_data[self.test_data["BRnum"] == br_num].iloc[0]
        result = download_single_pdf(
            brnum=str(test_row["BRnum"]), 
            primary_url=str(test_row["Pdf_URL"]), 
            secondary_url=str(test_row["Report Html Address"]), 
            output_folder=self.test_download_dir
        )
        self.assertEqual(result, ('Success', 'Secondary link OK; primary failed: No valid or malformed primary link'))
        file_count = len(os.listdir(self.test_download_dir))
        self.assertEqual(file_count, 1)

    @patch("logging.getLogger")
    @patch("threading.current_thread")
    @patch("pdf_downloader.downloader.parse_thread_name_to_id", return_value=1)
    def test_both_urls_fail(
        self, mock_logger, mock_thread, mock_parse, 
    ):
        br_num = "BR50277"
        test_row = self.test_data[self.test_data["BRnum"] == br_num].iloc[0]
        result = download_single_pdf(
            brnum=str(test_row["BRnum"]), 
            primary_url=str(test_row["Pdf_URL"]), 
            secondary_url=str(test_row["Report Html Address"]), 
            output_folder=self.test_download_dir
        )
        self.assertEqual(result, ("Failure", f"Both links failed. Primary=(GET request error: 403 Client Error: Forbidden for url: {test_row["Pdf_URL"]}); Secondary=(GET request error: 404 Client Error: Not Found for url: {test_row["Report Html Address"]})"))
        file_count = len(os.listdir(self.test_download_dir))
        self.assertEqual(file_count, 0)

    @patch("logging.getLogger")
    @patch("threading.current_thread")
    @patch("pdf_downloader.downloader.parse_thread_name_to_id", return_value=1)
    def test_no_valid_urls(
        self, mock_logger, mock_thread, mock_parse
    ):
        br_num = "BR50391"
        test_row = self.test_data[self.test_data["BRnum"] == br_num].iloc[0]
        
        result = download_single_pdf(
            brnum=str(test_row["BRnum"]), 
            primary_url=str(test_row["Pdf_URL"]), 
            secondary_url=str(test_row["Report Html Address"]), 
            output_folder=self.test_download_dir
        )
        
        self.assertEqual(result, ("Failure", "No valid or malformed primary link"))
        file_count = len(os.listdir(self.test_download_dir))
        self.assertEqual(file_count, 0)

if __name__ == "__main__":
    unittest.main()
