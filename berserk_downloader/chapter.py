"""Chapter Class"""

import os
import re
from datetime import date

import pydantic
import requests
from bs4 import BeautifulSoup, NavigableString

from berserk_downloader.image import Image


class Chapter(pydantic.BaseModel):
    """Chapter"""

    id: str
    name: str
    published_date: date
    url: str
    images: list[Image] = pydantic.Field(default_factory=list, init=False, repr=False)

    def __str__(self) -> str:
        """Representation"""
        return f"[>] Checking {self.name} at: {self.url}"

    def get_image_list(self) -> None:
        """Get images from chapter"""
        chapter_page = requests.get(self.url)
        soup = BeautifulSoup(chapter_page.text, features="html.parser")
        focus = soup.find("div", attrs={"class": "pages"})
        if not focus or isinstance(focus, NavigableString):
            return  # pragma: no cover
        images = focus.find_all("img", attrs={"class": "pages__img"})
        for i, img in enumerate(images):
            src = img.attrs.get("src").strip()
            if not src:
                continue
            img_name = src.split("/")[-1].split("?")[0]
            if not re.match(r"\d+\.\w{3,4}", img_name):
                img_name = f"{i + 1:03}.{img_name}"
            self.images.append(
                Image(
                    name=img_name,
                    chapter=re.sub(r"\W+", "-", self.name.lower()),
                    url=src,
                )
            )

    @staticmethod
    def create_root_dir() -> str:
        """Create root folder for downloading"""
        running_dir = os.getcwd()
        os.makedirs(os.path.join(running_dir, "Berserk"), exist_ok=True)
        return os.path.join(running_dir, "Berserk")

    def download(self):
        """Download chapter"""
        root_path = self.create_root_dir()
        for image in self.images:
            image.save(root_path=root_path)
