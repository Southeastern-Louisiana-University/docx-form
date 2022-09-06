from zipfile import ZipFile
from lxml import etree

Element = etree._Element

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
    xml_prefix: str = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

    # Unzip the file at path in append mode
    with ZipFile(path, "a") as docx:
        # The root of the document
        root: Element = etree.XML(docx.read("word/document.xml"))

        # The body of the document
        body: Element = root.getchildren()[0]

        # Print to text file at "C:\\Users\\reece\\Desktop\\testing.xml"
        """ with open(f"C:\\Users\\reece\\OneDrive\\Desktop\\{file_name}.xml", "w") as f:
            f.write(etree.tostring(root, pretty_print=True).decode("utf-8")) """

        # Loop through all tags within the <body> tag
        parent_tag: Element
        for parent_tag in body:
            # If the tag is a <w:sdt> tag, then it is a form field
            if parent_tag.tag == f"{xml_prefix}sdt":
                # Loop through all tags within the <w:sdt> tag
                child_tag: Element
                for child_tag in parent_tag:
                    if child_tag.tag == f"{xml_prefix}sdtPr":
                        # Determine the type of the field
                        grandchild_elements: list[Element] = child_tag.getchildren()
                        # Convert the Element object array to an array of strings
                        grandchild_tags: list[str] = [tag.tag for tag in grandchild_elements]

                        # If grandchild_tags contains the <w:date> tag, then it is a date picker field
                        if f"{xml_prefix}date" in grandchild_tags:
                            print("Date Picker Content Control")

                        # If grandchild_tags contains the <w:dropDownList> tag, then it is a drop down list field
                        elif f"{xml_prefix}dropDownList" in grandchild_tags:
                            print("Drop-Down Content Control")

                        # If grandchild_tags contains the <w:comboBox> tag, then it is a combo box field
                        elif f"{xml_prefix}comboBox" in grandchild_tags:
                            print("Combo Box Content Control")

                        # If grandchild_tags contains the <w:text> tag, then it is a plain text field
                        elif f"{xml_prefix}text" in grandchild_tags:
                            print("Plain Text Content Control")

                        # Otherwise, it is a rich text field
                        else:
                            print("Rich Text Content Control")

            # Also, if a <w:p> tag has a <w:sdt> tag as a child, then it is a Check Box Content Control
            if parent_tag.tag == f"{xml_prefix}p" and len(parent_tag.getchildren()) > 0:
                first_child = parent_tag.getchildren()[0].tag
                if first_child == f"{xml_prefix}sdt":
                    print("Check Box Content Control")
