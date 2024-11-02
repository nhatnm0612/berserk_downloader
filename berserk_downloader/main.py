"""Project entry point"""

import argparse
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, NavigableString

from berserk_downloader.chapter import Chapter
from berserk_downloader.constance import ROOT_URL


def main():
    """Calling package through command variables"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--chapters",
        type=str,
        help="Chapters separated by commas. Eg: 001,002,003... Leave it blank to download all",
        default="all",
    )
    args = parser.parse_args()
    if args.chapters != "all":
        args.chapters = args.chapters.split(",")
    return downloader(chapters=args.chapters)


def downloader(chapters: list[str] | str = []) -> int:
    """Downloader"""
    root_page = requests.get(ROOT_URL)
    soup = BeautifulSoup(root_page.text, features="html.parser")
    focus = soup.find("tbody", attrs={"class": "no-border-x"})
    if not focus or isinstance(focus, NavigableString):
        return 0  # pragma: no cover
    for tr in focus.find_all("tr"):
        chap_name = tr.find_all("td")[0].get_text()
        chap_published_date = tr.find_all("td")[1].get_text()
        chap_url = tr.find("a").attrs.get("href")
        _id = re.findall(r"Berserk Chapter (\S+)", chap_name)[0]
        if chapters != "all" and _id not in chapters:
            continue
        chapter = Chapter(
            id=_id,
            name=chap_name,
            published_date=datetime.strptime(chap_published_date, "%b %d, %Y"),
            url=chap_url,
        )
        print(chapter)
        chapter.get_image_list()
        chapter.download()

    return 0


if __name__ == "__main__":
    main()
