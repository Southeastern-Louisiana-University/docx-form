# Package Imports
from zipfile import ZipFile
from lxml import etree
import re

# Local Imports (don't forget the "." in front of the module name)
try:
    from enums import TagType
except ImportError:
    from .enums import TagType

# Type Aliases
Element = etree._Element

# Constants
XML_PREFIX = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class DocxForm:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = self.__verify_path(file_path)
        # Note: this will become a list[DocxContentControl] in a later version
        self.content_control_forms: list[
            Element
        ] = self.__get_all_content_control_forms()

    def __verify_path(self, file_path: str):
        # regex to check for docx extension in file path
        verify = re.compile("\\.docx")

        if not verify.search(file_path):
            raise Exception("File is not docx")

        # File path verify with file open attempt

        try:
            open(file_path, "a")

        except OSError:
            ...

            # Zipfile ops at self.file_path and open xml

        with ZipFile(file_path) as myzip:
            with myzip.open("word/document.xml") as myfile:
                myfile.read()

        return file_path

    def __get_all_content_control_forms(self) -> list[Element]:
        with ZipFile(self.file_path) as document:
            # Return variable
            content_control_forms: list[Element] = []
            # The root of the document
            root: Element = etree.XML(document.read("word/document.xml"))
            # The body of the document
            body: Element = root.getchildren()[0]

            # Loop through all tags within the <body> tag
            parent_tag: Element
            for parent_tag in body:
                # If the tag is a <w:sdt> tag, then it is a form field
                if parent_tag.tag == f"{XML_PREFIX}sdt":
                    content_control_forms.append(
                        self.__determine_content_control(parent_tag, TagType.SDT)
                    )

                # Also, if a <w:p> tag has a <w:sdt> tag as a child, then it is a Check Box Content Control
                if (
                    parent_tag.tag == f"{XML_PREFIX}p"
                    and len(parent_tag.getchildren()) > 0
                ):
                    content_control_forms.append(
                        self.__determine_content_control(parent_tag, TagType.P)
                    )

            # Remove the None values from the list ()
            content_control_forms = [x for x in content_control_forms if x is not None]

            return content_control_forms

    # Note: this will have a specific return type in a later version that corresponds to the type of content control
    def __determine_content_control(
        self, parent_tag: Element, tag_type: TagType
    ) -> Element | None:
        match tag_type:
            # Loop through all tags within the <w:sdt> tag
            case TagType.SDT:
                child_tag: Element
                for child_tag in parent_tag:
                    if child_tag.tag == f"{XML_PREFIX}sdtPr":
                        # Determine the type of the field
                        grandchild_elements: list[Element] = child_tag.getchildren()
                        # Convert the Element object array to an array of strings
                        grandchild_tags: list[str] = [
                            tag.tag for tag in grandchild_elements
                        ]

                        # If grandchild_tags contains the <w:date> tag, then it is a date picker field
                        if f"{XML_PREFIX}date" in grandchild_tags:
                            print("Date Picker Content Control")
                            return parent_tag  # TODO: Replace with a DatePickerContentControl object
                        # If grandchild_tags contains the <w:dropDownList> tag, then it is a drop down list field
                        elif f"{XML_PREFIX}dropDownList" in grandchild_tags:
                            print("Drop-Down Content Control")
                            return parent_tag  # TODO: Replace with a DropDownListContentControl object
                        # If grandchild_tags contains the <w:comboBox> tag, then it is a combo box field
                        elif f"{XML_PREFIX}comboBox" in grandchild_tags:
                            print("Combo Box Content Control")
                            return parent_tag  # TODO: Replace with a ComboBoxContentControl object
                        # If grandchild_tags contains the <w:text> tag, then it is a plain text field
                        elif f"{XML_PREFIX}text" in grandchild_tags:
                            print("Plain Text Content Control")
                            return parent_tag  # TODO: Replace with a PlainTextContentControl object
                        # Otherwise, it is a rich text field
                        else:
                            print("Rich Text Content Control")
                            return parent_tag  # TODO: Replace with a RichTextContentControl object

            # Check if the first child of the <w:p> tag is a <w:sdt> tag
            case TagType.P:
                first_child: str = parent_tag.getchildren()[0].tag
                if first_child == f"{XML_PREFIX}sdt":
                    print("Check Box Content Control")
                    return (
                        parent_tag  # TODO: Replace with a CheckBoxContentControl object
                    )
                else:
                    return None


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    ...
