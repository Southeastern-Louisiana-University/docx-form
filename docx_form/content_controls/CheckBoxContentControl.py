# Local Imports
from .DocxContentControl import DocxContentControl

# Package Imports
from lxml import etree

try:
    from type_aliases import Element
    from constants import XML_PREFIX, XML_CHECK
    from globals import Raw_XML
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX, XML_CHECK
    from ..globals import Raw_XML


class CheckBoxContentControl(DocxContentControl):
    """
    This class contains the properties and functions associated with the Check Box content control.

    :param DocxContentControl: This class extends DocxContentControl
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)

    def set_checkBox(self, check_value: bool):
        """
        This method sets a checkbox to checked or unchecked on a CheckBox Content Control

        :param bool check_value: Sets checkbox to checked for true and unchecked for false
        """

        # Set values according to the boolean passed in
        if check_value == True:
            checkBoxVal = "1"
            box = "☒"
        else:
            checkBoxVal = "0"
            box = "☐"

        # The root of the document
        root: Element = etree.XML(Raw_XML.raw_xml)
        # The body of the document
        body: Element = root.getchildren()[0]

        element: Element
        for element in body.iter(f"{XML_PREFIX}sdt"):
            # Get the nested id tag
            id_tag: Element
            for id_tag in element.iter(f"{XML_PREFIX}id"):
                # If the id matches
                if id_tag.get(f"{XML_PREFIX}val") == self.id:
                    # Set attribute value
                    match: Element
                    for match in element.iter(f"{XML_CHECK}checked"):
                        match.set(f"{XML_CHECK}val", checkBoxVal)

                    # Replace the text
                    for match in element.iter(f"{XML_PREFIX}t"):
                        match.text = box

        # Write the new document to raw_xml
        Raw_XML.raw_xml = etree.tostring(root)
