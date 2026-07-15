import requests
import json
import csv

from .extractor import Extractor
from .exceptions import WoopConnectionError
from .cleaner import Cleaner



class Scrap:


    def __init__(
        self,
        url,
        timeout=10
    ):

        self.url = url
        self.timeout = timeout

        self.html = self._fetch()

        self.extractor = Extractor(
            self.html
        )

        self.cleaner = Cleaner()



    def _fetch(self):

        try:

            response = requests.get(
                self.url,
                timeout=self.timeout,
                headers={
                    "User-Agent": "WoopScraper/0.1"
                }
            )

            response.raise_for_status()

            return response.text


        except Exception as e:

            raise WoopConnectionError(
                str(e)
            )



    def title(self):

        return self.extractor.title()



    def links(self):

        links = self.extractor.links()

        return self.cleaner.clean_list(
            links
        )



    def text(self):

        text = self.extractor.text()

        return self.cleaner.clean_text(
            text
        )



    def images(self):

        images = self.extractor.images()

        return self.cleaner.clean_list(
            images
        )



    def emails(self):

        emails = self.extractor.emails()

        return self.cleaner.clean_list(
            emails
        )

    def extract(self):

        return {

            "url": self.url,

            "title": self.title(),

            "text": self.text(),

            "links": self.links(),

            "email": self.emails()

        }

    def export_json(
            self,
            filename="result.json"
    ):

        data = self.extract()

        with open(
                filename,
                "w",
                encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return filename

    def export_csv(
            self,
            filename="result.csv"
    ):

        data = self.extract()

        with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # écrire les colonnes
            writer.writerow(
                [
                    "field",
                    "value"
                ]
            )

            # écrire les données
            for key, value in data.items():

                if isinstance(value, list):

                    value = ", ".join(value)


                elif isinstance(value, dict):

                    value = json.dumps(
                        value,
                        ensure_ascii=False
                    )

                writer.writerow(
                    [
                        key,
                        value
                    ]
                )

        return filename