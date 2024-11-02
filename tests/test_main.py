"""Test Entry"""

import argparse
import os
from unittest.mock import patch

import requests

import berserk_downloader.main as berserk_downloader
from berserk_downloader.chapter import Chapter


@patch.object(argparse.ArgumentParser, "parse_args")
def test_main(mock_args):
    """Testing code"""
    args = argparse.Namespace(chapters="001,002")
    mock_args.return_value = args
    with patch.object(berserk_downloader, "downloader", return_value=0):
        berserk_downloader.main()


@patch.object(requests, "get")
def test_downloader(mock_get):
    """Testing code"""
    resp = requests.Response()
    resp.status_code = 200
    cwd = os.path.dirname(os.path.abspath(__file__))
    test_page = os.path.join(cwd, "local_html_pages/test_home.html")
    with open(test_page, "rb") as test_content:
        resp._content = test_content.read()
    mock_get.return_value = resp
    with patch.object(Chapter, "get_image_list", return_value=None):
        with patch.object(Chapter, "download", return_value=None):
            berserk_downloader.downloader(chapters=["001", "002"])
