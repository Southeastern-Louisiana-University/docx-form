# Package Imports
from zipfile import ZipFile
from lxml import etree
import re, os

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
    from form_fields import TextFormField, CheckBoxFormField, DropDownFormField
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
    from .form_fields import TextFormField, CheckBoxFormField, DropDownFormField
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
FormField = CheckBoxFormField | DropDownFormField | TextFormField


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
        self.content_control_forms_and_form_fields: list[
            ContentControl | FormField
        ] = self.__get_all_content_control_forms_and_form_fields()

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

    def list_all_content_controls_and_form_fields(self):
        """
        This method prints all content controls and form fields in the document.
        """

        # Track current array index in for loop
        pos = 0
        # print values from each control with the index in content_control_forms
        for control in self.content_control_forms_and_form_fields:
            if isinstance(control, ContentControl):
                print(
                    str(pos)
                    + ": "
                    + control.__class__.__name__
                    + " | id: "
                    + control.id
                    + " | text: "
                    + control.text
                )
            else:
                print(
                    str(pos)
                    + ": "
                    + control.__class__.__name__
                    + " | name: "
                    + control.name
                    + " | value: "
                    + control.value
                )
            pos = pos + 1

    def __get_raw_xml(self) -> str:
        """
        This method returns the raw xml of the document.

        :return str: The raw xml of the document
        """
        with ZipFile(self.file_path) as document:
            # Put the raw xml into an xml file for testing
            full_path = ""
            if len(full_path) > 0:
                with open(full_path, "wb") as f:
                    f.write(document.read("word/document.xml"))

            return document.read(
                "word/document.xml"
            )  # .decode("utf-8") this creates problems for some reason

    def __verify_path(self, file_path: str) -> str:
        """
        This method verifies that the file path is valid.

        :param str file_path: The path to the document
        :raises Exception: If the file path is not to a .docx file
        :return str: The file path
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

    def __get_all_content_control_forms_and_form_fields(self) -> list[ContentControl]:
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
            p_tag: Element
            for p_tag in body.iter(f"{XML_PREFIX}p"):
                """
                Note: The same <w:p> tag can be used for multiple checkboxes depending on the document.
                The name value will differentiate them.
                """
                child: Element
                for child in p_tag.iter(f"{XML_PREFIX}name"):
                    content_control_forms.append(
                        self.__determine_content_control(
                            p_tag, TagType.P, child.get(f"{XML_PREFIX}val")
                        )
                    )

            # Remove the None values from the list ()
            content_control_forms = [x for x in content_control_forms if x is not None]

            return content_control_forms

    def __determine_content_control(
        self, parent_tag: Element, tag_type: TagType, name: str = ""
    ) -> ContentControl | FormField | None:
        """
        This method determines the type of content control and returns the appropriate object.

        :param Element parent_tag: The parent tag of the content control. This will be a <w:sdt> tag or a <w:p> tag.
        :param TagType tag_type: The type of tag that the content control is in. This will be either SDT or P.
        :param str name: The name of the content control. This is only used for form fields.
        :return: The content control or form field object
        :rtype: ContentControl | FormField | None
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

            # This case handles all Form Fields
            case TagType.P:
                # Find a Text Form Field if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}textInput"):
                    return TextFormField(parent_tag, self.file_path, name)

                # Find a Drop Down Form Field if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}ddList"):
                    return DropDownFormField(parent_tag, self.file_path, name)

                # Find a Check Box Form Field if it exists
                for child in parent_tag.iter(f"{XML_PREFIX}checkBox"):
                    # return CheckBoxFormField(parent_tag, self.file_path, name)
                    # TODO: Find a way to differentiate checkboxes from each other reliably
                    return None


# Use this for debugging, then move to a test file.
# This will run if you run this file directly.
if __name__ == "__main__":
    ...
