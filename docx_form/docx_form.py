from zipfile import ZipFile
from lxml import etree


class DocxForm:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def print_path(self) -> None:
        print(self.file_path)


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    ...
