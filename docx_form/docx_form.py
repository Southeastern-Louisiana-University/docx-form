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
    from constants import XML_PREFIX, XML_CHECK
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
    from .constants import XML_PREFIX, XML_CHECK
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
    """
    This is the one and only entry point for the DocxForm package.
    DocxForm holds all content controls for a given document and allows read and write operations on the document.
    """

    def __init__(self, file_path: str):
        """
        This initalizes the DocxForm class.

        :param str file_path: The path to the document
        """

        self.file_path: str = self.__verify_path(file_path)
        Raw_XML.raw_xml = self.__get_raw_xml()
        self.content_control_forms: list[
            ContentControl
        ] = self.__get_all_content_control_forms()

    def save(self, destination_path: str | None = None):
        """
        This method saves the document to the destination path if a path is given.
        If not, the original file is overwritten.
        :param str destination_path: The full path to save the file to, defaults to None
        """

        # If no name is given the original docx will be overwritten
        if (
            destination_path == None
            or destination_path == " "
            or destination_path == ""
        ):
            temp_path = self.file_path.replace(".docx", "-temp.docx")

            with ZipFile(self.file_path, "a") as doc, ZipFile(
                temp_path, "w"
            ) as temp_doc:
                # Copy all contents except the "word/document.xml" file from the docx to the temp docx
                doc_list = doc.infolist()
                for item in doc_list:
                    if item.filename != "word/document.xml":
                        temp_doc.writestr(item, doc.read(item.filename))
                # Write changes to new docx
                temp_doc.writestr("word/document.xml", Raw_XML.raw_xml)

            # Delete the original docx
            os.remove(self.file_path)

            # Rename the temporary docx to match the original name
            os.renames(temp_path, self.file_path)

        # Saves to a new file -- uses path as destination, relative path does work
        else:
            # Replace document path with the destination path
            new_path = destination_path

            with ZipFile(self.file_path, "a") as old_doc, ZipFile(
                new_path, "w"
            ) as new_doc:
                # Copy all contents except the "word/document.xml" file from the old docx to the new docx
                doc_list = old_doc.infolist()
                for item in doc_list:
                    if item.filename != "word/document.xml":
                        new_doc.writestr(item, old_doc.read(item.filename))
                # Write changes to new docx
                new_doc.writestr("word/document.xml", Raw_XML.raw_xml)

    def list_all_content_controls(self):
        """
        This method prints all content controls in the document.
        """

        # Track current array index in for loop
        pos = 0
        # print values from each control with the index in content_control_forms
        for control in self.content_control_forms:
            print(
                str(pos)
                + ": "
                + control.type
                + ". id: "
                + control.id
                + ". text: "
                + control.text
            )
            pos = pos + 1

    def __get_raw_xml(self) -> str:
        """
        This method returns the raw xml of the document.

        :return str: The raw xml of the document
        """
        with ZipFile(self.file_path) as document:
            # Put the raw xml into an xml file for testing
            # TODO: Delete when publishing package
            """full_path = (
                "C:/Users/reece/Desktop/test_file.xml"  # TODO: Delete me!
            )"""
            full_path = ""
            if len(full_path) > 0:
                with open(full_path, "wb") as f:
                    f.write(document.read("word/document.xml"))

            return document.read(
                "word/document.xml"
            )  # .decode("utf-8") this creates problems for some reason

    def __verify_path(self, file_path: str):
        """
        This method verifies that the file path is valid.

        :param str file_path: The path to the document
        :raises Exception: If the file path is not to a .docx file
        :return _type_: The file path
        """
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
        """
        This method returns all content control forms in the document.

        :return list[ContentControl]:
        """
        with ZipFile(self.file_path) as document:
            # Return variable
            content_control_forms: list[ContentControl] = []
            # The root of the document
            root: Element = etree.XML(document.read("word/document.xml"))
            # The body of the document
            body: Element = root.getchildren()[0]

            # Find all content controls in the document
            content_control: Element
            for content_control in body.iter(f"{XML_PREFIX}sdt"):
                content_control_forms.append(
                    self.__determine_content_control(content_control, TagType.SDT)
                )

            # Find all form fields in the document
            form_field: Element
            for form_field in body.iter(f"{XML_PREFIX}p"):
                content_control_forms.append(
                    self.__determine_content_control(form_field, TagType.P)
                )

            """ OLD START
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

            OLD END """

            # Remove the None values from the list ()
            content_control_forms = [x for x in content_control_forms if x is not None]

            return content_control_forms

    # Note: this will have a specific return type in a later version that corresponds to the type of content control
    def __determine_content_control(
        self, parent_tag: Element, tag_type: TagType
    ) -> ContentControl | None:
        """
        This method determines the type of content control and returns the appropriate object.

        :param Element parent_tag: The parent tag of the content control. This will be a <w:sdt> tag or a <w:p> tag.
        :param TagType tag_type: The type of tag that the content control is in. This will be either SDT or P.
        :return ContentControl | None: The content control object
        """

        child: Element

        match tag_type:
            # This case handles all Content Control types
            case TagType.SDT:
                # Find a Date Picker Content Control if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}date"):
                    return DatePickerContentControl(parent_tag, self.file_path)

                # Find a Drop Down List Content Control if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}dropDownList"):
                    return DropDownListContentControl(parent_tag, self.file_path)

                # Find a Combo Box Content Control if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}comboBox"):
                    return ComboBoxContentControl(parent_tag, self.file_path)

                # Find a Plain Text Content Control if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}text"):
                    return PlainTextContentControl(parent_tag, self.file_path)

                # Find a Check Box Content Control if it exists
                for child in parent_tag.iter(f"{XML_CHECK}checkbox"):
                    return CheckBoxContentControl(parent_tag, self.file_path)

                # Otherwise, it is a Rich Text Content Control
                return RichTextContentControl(parent_tag, self.file_path)

            # This case handles all Form Field types
            case TagType.P:
                for child in parent_tag.iter(f"{XML_PREFIX}instrText"):
                    print(child)
                    """print("p - instrText")
                    print(child)"""

                """OLD START
                first_child: str = parent_tag.getchildren()[0].tag
                if first_child == f"{XML_PREFIX}sdt":
                    return CheckBoxContentControl(
                        parent_tag.getchildren()[0], self.file_path
                    )
                else:
                    return None
                OLD END"""


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    full_path = "C:/Users/reece/Desktop/change_cat_request.docx"
    # full_path = "C:/Users/reece/git_repos/docx-form/docx_form_tests/test.docx"
    document = DocxForm(full_path)

    # Print all content control forms
    # document.list_all_content_controls()
