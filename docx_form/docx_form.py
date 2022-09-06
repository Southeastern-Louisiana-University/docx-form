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
    file_name: str = "test"
    path: str = f"C:\\Users\\reece\\OneDrive\\Desktop\\{file_name}.docx"
    docx_form = DocxForm(path)

    # Unzip the file at path in append mode
    with ZipFile(path, "a") as docx:
        # The root of the document
        root = etree.XML(docx.read("word/document.xml"))
        # The body of the document
        body = root.getchildren()[0]

        # Print to text file at "C:\\Users\\reece\\Desktop\\testing.xml"
        """ with open(f"C:\\Users\\reece\\OneDrive\\Desktop\\{file_name}.xml", "w") as f:
            f.write(etree.tostring(root, pretty_print=True).decode("utf-8")) """

        # Loop through all tags within the <body> tag
        for tag in body:
            # If the tag is a <w:sdt> tag, then it is a form field
            if (
                tag.tag
                == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sdt"
            ):
                print("Form field")

            # Also, if a <w:p> tag has a <w:sdt> tag as a child, then it is a form field
            if (
                tag.tag
                == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
                and len(tag.getchildren()) > 0
            ):
                first_child = tag.getchildren()[0].tag
                if (
                    first_child
                    == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sdt"
                ):
                    print("Check Box Content Control")
