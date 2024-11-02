"""Test Chapter Class"""

import os
from unittest.mock import patch

import requests

import berserk_downloader
from berserk_downloader.chapter import Chapter, date
from berserk_downloader.image import Image


class TestChapter:
    """Test Chapter"""

    chapter = Chapter(
        id="001",
        name="berserk-chapter-001",
        published_date=date(2000, 1, 1),
        url="https://fake-url.local",
    )

    def test___str__(self):
        """Testing code"""
        _str = "[>] Checking berserk-chapter-001 at: https://fake-url.local"
        assert self.chapter.__str__() == _str

    @patch.object(requests, "get")
    def test_get_image_list(self, mock_get):
        """Testing code"""
        resp = requests.Response()
        resp.status_code = 200
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_page = os.path.join(cwd, "local_html_pages/test_page.html")
        with open(test_page, "rb") as test_content:
            resp._content = test_content.read()
        mock_get.return_value = resp
        assert self.chapter.images == []
        self.chapter.get_image_list()
        assert len(self.chapter.images) == 20
        for image in self.chapter.images:
            assert isinstance(image, Image)

    @patch.object(Image, "save")
    def test_download(self, mock_save):
        """Testing code"""
        mock_save.return_value = None
        self.chapter.download()
        project_path = os.path.abspath(berserk_downloader.__file__)
        download_dir = os.path.join(
            os.path.dirname(os.path.dirname(project_path)), "Berserk"
        )
        assert os.path.isdir(download_dir)
