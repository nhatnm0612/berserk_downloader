"""Testing Image Class"""

import os
from unittest.mock import patch

import requests

from berserk_downloader.image import Image


class TestImage:
    """Testing Image"""

    image = Image(
        name="1.jpg",
        chapter="001",
        url="https://fake-url.local",
    )

    def test___str__(self):
        """Testing code"""
        _str = "Image 1.jpg of Chapter 001"
        assert self.image.__str__() == _str

    @patch.object(requests, "get")
    def test_save(self, mock_get):
        """Testing code"""
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"0101"
        mock_get.return_value = resp
        root_path = os.path.dirname(os.path.abspath(__file__))
        chapter_path = os.path.join(root_path, "001")
        image_path = os.path.join(chapter_path, "1.jpg")
        assert not os.path.exists(chapter_path)
        assert not os.path.exists(image_path)
        self.image.save(root_path)
        assert os.path.exists(chapter_path)
        assert os.path.exists(image_path)
        self.image.save(root_path)
        os.remove(image_path)
        os.removedirs(chapter_path)
