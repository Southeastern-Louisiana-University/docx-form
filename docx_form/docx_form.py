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
    path: str = "C:\\Users\\reece\\Desktop\\testing.docx"
    docx_form = DocxForm(path)

    # Unzip the file at path in append mode
    with ZipFile(path, "a") as docx:
        root = etree.XML(docx.read("word/document.xml"))
        
        # Print to text file at "C:\\Users\\reece\\Desktop\\testing.xml"
        with open("C:\\Users\\reece\\Desktop\\testing.xml", "w") as f:
            f.write(etree.tostring(root, pretty_print=True).decode("utf-8"))
