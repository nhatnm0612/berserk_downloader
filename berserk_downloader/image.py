"""Image Class"""

import os

import pydantic
import requests


class Image(pydantic.BaseModel):
    """Image"""

    name: str
    chapter: str
    url: str

    def __str__(self) -> str:
        """Representation"""
        return f"Image {self.name} of Chapter {self.chapter}"

    def save(self, root_path: str) -> None:
        """Download single image"""
        chapter_path = os.path.join(root_path, self.chapter)
        if not os.path.exists(chapter_path):
            os.mkdir(chapter_path)
        file_path = os.path.join(chapter_path, self.name)
        if os.path.exists(file_path):
            return
        img = requests.get(self.url)
        content = img.content
        with open(file=file_path, mode="wb") as f:
            f.write(content)
