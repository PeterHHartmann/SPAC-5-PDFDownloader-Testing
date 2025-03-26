import os
from queue import Queue
import shutil
import threading
import unittest

from ui.app import DownloadApp
from pdf_downloader.downloader import run_downloader


class TestRunDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = ["tests/test_data/GRI_sample.xlsx", "tests/test_data/Metadata_sample.xlsx"]
        cls.test_download_dir="tests/temp/PDFs"
        cls.test_status_file_dir = "tests/temp/DownloadedStatus.xlsx"

    @classmethod
    def tearDownClass(cls):
        os.mkdir(cls.test_data_dir)
        shutil.rmtree(cls.test_data_dir) # Remove test files after tests

    def test_pdfs_downloaded(self):
        update_queue = Queue()
        app = DownloadApp(
            update_queue=update_queue,
            max_workers=3,
            max_success=10,
            dev_mode=True
        )
        def idk():
            run_downloader(
                xlsx_paths=self.test_data,
                output_folder=self.test_download_dir,
                status_file=self.test_status_file_dir,
                max_success=10,
                max_concurrent_workers=3,
                update_queue=update_queue,
                dev_mode=True,
                chunk_size=1000
            )
        thread = threading.Thread(target=idk, daemon=True)
        thread.start()
        app.mainloop()
        thread.join()
        downloaded_files = os.listdir(self.test_download_dir)
        self.assertEqual(len(downloaded_files), 10)


