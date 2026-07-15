from bs4 import BeautifulSoup
import re


class Extractor:

    def __init__(self, html):
        self.soup = BeautifulSoup(
            html,
            "lxml"
        )


    def title(self):

        if self.soup.title:
            return self.soup.title.text.strip()

        return None


    def links(self):

        links = []

        for link in self.soup.find_all("a"):
            href = link.get("href")

            if href:
                links.append(href)

        return links


    def text(self):

        return self.soup.get_text(
            separator=" ",
            strip=True
        )


    def images(self):

        images = []

        for img in self.soup.find_all("img"):

            src = img.get("src")

            if src:
                images.append(src)

        return images

    def emails(self):

        text = self.soup.get_text()

        return re.findall(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            text
        )