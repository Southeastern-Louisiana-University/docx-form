# Package Imports
from zipfile import ZipFile
from lxml import etree
import re, os

# Local Imports
try:
    from enums import TagType
    from content_controls import (
        PlainTextContentControl,
        RichTextContentControl,
        ComboBoxContentControl,
        DropDownListContentControl,
        CheckBoxContentControl,
        DatePickerContentControl,
    )
    from constants import XML_PREFIX
    from globals import Raw_XML
    from type_aliases import Element
except ImportError:
    from .enums import TagType
    from .content_controls import (
        PlainTextContentControl,
        RichTextContentControl,
        ComboBoxContentControl,
        DropDownListContentControl,
        CheckBoxContentControl,
        DatePickerContentControl,
    )
    from .constants import XML_PREFIX
    from .globals import Raw_XML
    from .type_aliases import Element

# Local Type Aliases
ContentControl = (
    CheckBoxContentControl
    | RichTextContentControl
    | ComboBoxContentControl
    | DatePickerContentControl
    | DropDownListContentControl
    | PlainTextContentControl
)


class DocxForm:
    def __init__(self, file_path: str):
        self.file_path: str = self.__verify_path(file_path)
        Raw_XML.raw_xml = self.__get_raw_xml()
        self.content_control_forms: list[
            ContentControl
        ] = self.__get_all_content_control_forms()

    def save(self, file_append=None):

        if file_append == None:
            temp_path = self.file_path.replace(".docx", "-temp.docx")

            with ZipFile(self.file_path, "a") as doc, ZipFile(
                temp_path, "w"
            ) as temp_doc:
                # Copy all contents ecxept the "word/document.xml" file from the docx to the temp docx
                doc_list = doc.infolist()
                for item in doc_list:
                    if item.filename != "word/document.xml":
                        temp_doc.writestr(item, doc.read(item.filename))
                # Write changes to new docx
                temp_doc.writestr("word/document.xml", Raw_XML.raw_xml)
            os.remove(self.file_path)
            os.renames(temp_path, self.file_path)

        # Saves to a new file
        else:
            # Replace .docx with "file_append.docx" in the file path
            new_path = self.file_path.replace(".docx", file_append + ".docx")

            with ZipFile(self.file_path, "a") as old_doc, ZipFile(
                new_path, "w"
            ) as new_doc:
                # Copy all contents ecxept the "word/document.xml" file from the old docx to the new docx
                doc_list = old_doc.infolist()
                for item in doc_list:
                    if item.filename != "word/document.xml":
                        new_doc.writestr(item, old_doc.read(item.filename))
                # Write changes to new docx
                new_doc.writestr("word/document.xml", Raw_XML.raw_xml)

    def __get_raw_xml(self) -> str:
        with ZipFile(self.file_path) as document:
            # Put the raw xml into an xml file for testing
            full_path = ""
            if len(full_path) > 0:
                with open(full_path, "wb") as f:
                    f.write(document.read("word/document.xml"))

            return document.read(
                "word/document.xml"
            )  # .decode("utf-8") this creates problems for some reason #

    def __verify_path(self, file_path: str):
        # regex to check for docx extension in file path
        verify = re.compile("\\.docx$")

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

    def __get_all_content_control_forms(self) -> list[ContentControl]:
        with ZipFile(self.file_path) as document:
            # Return variable
            content_control_forms: list[ContentControl] = []
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
    ) -> ContentControl | None:
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
                            return DatePickerContentControl(parent_tag, self.file_path)
                        # If grandchild_tags contains the <w:dropDownList> tag, then it is a drop down list field
                        elif f"{XML_PREFIX}dropDownList" in grandchild_tags:
                            return DropDownListContentControl(
                                parent_tag, self.file_path
                            )
                        # If grandchild_tags contains the <w:comboBox> tag, then it is a combo box field
                        elif f"{XML_PREFIX}comboBox" in grandchild_tags:
                            return ComboBoxContentControl(parent_tag, self.file_path)
                        # If grandchild_tags contains the <w:text> tag, then it is a plain text field
                        elif f"{XML_PREFIX}text" in grandchild_tags:
                            return PlainTextContentControl(parent_tag, self.file_path)
                        # Otherwise, it is a rich text field
                        else:
                            return RichTextContentControl(parent_tag, self.file_path)

            # Check if the first child of the <w:p> tag is a <w:sdt> tag
            case TagType.P:
                first_child: str = parent_tag.getchildren()[0].tag
                if first_child == f"{XML_PREFIX}sdt":
                    return CheckBoxContentControl(
                        parent_tag.getchildren()[0], self.file_path
                    )
                else:
                    return None


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    ...
