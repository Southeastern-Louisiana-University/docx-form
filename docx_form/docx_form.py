from zipfile import ZipFile
from lxml import etree
import re


class DocxForm:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        # regex to check for docx extension in file path

        verify = re.compile("\.docx")

        if verify.search(self.file_path):
            print("File is docx")

        else:
            raise Exception("File is not docx")

        # File path verify 

        try:
            open(self.file_path, "a")
            print("File Path is valid")

        except OSError:
            raise Exception("File Path is not valid")

        # Zipfile ops at self.file_path
        
        with ZipFile(self.file_path) as myzip:
            with myzip.open("word/document.xml") as myfile:
                print(myfile.read())

    def print_path(self) -> None:
        print(self.file_path)


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    ...
