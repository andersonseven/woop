import re


class Cleaner:


    @staticmethod
    def clean_text(text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()



    @staticmethod
    def clean_list(items):

        return list(
            set(
                item.strip()
                for item in items
                if item
            )
        )