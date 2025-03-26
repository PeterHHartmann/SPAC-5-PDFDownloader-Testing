import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil
import requests
import PyPDF2
from pdf_downloader.downloader import attempt_download

class TestAttemptDownload(unittest.TestCase):
    
    @patch("requests.get")
    @patch("requests.head")
    @patch("shutil.disk_usage")
    def test_successful_download(self, mock_disk_usage, mock_head, mock_get):
        file_path = Path("/tmp/test.pdf")
        url = "https://example.com/test.pdf"
        brnum = 1
        
        # Mock sufficient disk space
        mock_disk_usage.return_value = shutil.disk_usage("/")
        
        # Mock HEAD request
        mock_head_resp = MagicMock()
        mock_head_resp.headers = {"Content-Type": "application/pdf", "Content-Length": "2000"}
        mock_head_resp.raise_for_status = MagicMock()
        mock_head.return_value = mock_head_resp
        
        # Mock GET request
        mock_get_resp = MagicMock()
        mock_get_resp.iter_content = MagicMock(return_value=[b"%PDF-", b"test content"])
        mock_get_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_get_resp
        
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            with patch("PyPDF2.PdfReader") as mock_pdf_reader:
                mock_pdf_reader.return_value.pages = [1]
                result = attempt_download(file_path, url, brnum)
                
                self.assertEqual(result, ("Success", ""))
                mock_file.assert_called_once_with(file_path, "wb")
                mock_pdf_reader.assert_called_once()
    
    # def test_invalid_url(self):
    #     file_path = Path("/tmp/test.pdf")
    #     url = "invalid_url"
    #     brnum = 1
    #     result = attempt_download(file_path, url, brnum)
    #     self.assertEqual(result, ("Failure", "URL is missing http/https protocol or malformed."))
    
    # @patch("pdf_downloader.downloader.shutil.disk_usage")
    # def test_insufficient_disk_space(self, mock_disk_usage):
    #     file_path = Path("/tmp/test.pdf")
    #     url = "https://example.com/test.pdf"
    #     brnum = 1
        
    #     # Mock low disk space
    #     mock_disk_usage.return_value = shutil.disk_usage("/")._replace(free=4 * 1024 * 1024)
        
    #     result = attempt_download(file_path, url, brnum)
    #     self.assertEqual(result, ("Failure", "Insufficient disk space."))
    
    # @patch("pdf_downloader.downloader.requests.get")
    # def test_failed_get_request(self, mock_get):
    #     file_path = Path("/tmp/test.pdf")
    #     url = "https://example.com/test.pdf"
    #     brnum = 1
        
    #     mock_get.side_effect = requests.exceptions.RequestException("GET request error")
        
    #     result = attempt_download(file_path, url, brnum)
    #     self.assertEqual(result, ("Failure", "GET request error: GET request error"))
    
    # @patch("pdf_downloader.downloader.requests.get")
    # @patch("pdf_downloader.downloader.requests.head")
    # def test_missing_pdf_signature(self, mock_head, mock_get):
    #     file_path = Path("/tmp/test.pdf")
    #     url = "https://example.com/test.pdf"
    #     brnum = 1
        
    #     # Mock HEAD request
    #     mock_head_resp = MagicMock()
    #     mock_head_resp.headers = {"Content-Type": "application/pdf"}
    #     mock_head.return_value = mock_head_resp
        
    #     # Mock GET request
    #     mock_get_resp = MagicMock()
    #     mock_get_resp.iter_content = MagicMock(return_value=[b"not a pdf"])
    #     mock_get.return_value = mock_get_resp
        
    #     result = attempt_download(file_path, url, brnum)
    #     self.assertEqual(result, ("Failure", "No %PDF- signature in the initial data."))
    
    # @patch("pdf_downloader.downloader.PyPDF2.PdfReader")
    # def test_pypdf2_parse_error(self, mock_pdf_reader):
    #     file_path = Path("/tmp/test.pdf")
    #     url = "https://example.com/test.pdf"
    #     brnum = 1
        
    #     with patch("builtins.open", unittest.mock.mock_open(read_data=b"%PDF-test")):
    #         mock_pdf_reader.side_effect = Exception("Invalid PDF structure")
    #         result = attempt_download(file_path, url, brnum)
    #         self.assertEqual(result, ("Failure", "PyPDF2 parse error: Invalid PDF structure"))

if __name__ == "__main__":
    unittest.main()