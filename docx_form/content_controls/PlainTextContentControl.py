# Package Imports
from lxml import etree

# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
    from constants import XML_PREFIX
    from globals import Raw_XML
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX
    from ..globals import Raw_XML


class PlainTextContentControl(DocxContentControl):
    """
    This class contains all properties and methods for a Plain Text content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.type = "Plain Text Content Control"

    def set_text(self, new_text: str):
        """
        This method sets the text of a Plain Text content control.

        :param str new_text: The new text to set
        """

        # The root of the document
        root: Element = etree.XML(Raw_XML.raw_xml)
        # The body of the document
        body: Element = root.getchildren()[0]

        # Find the plain text content control with the same id as self
        element: Element
        for element in body.getchildren():
            if element.tag == f"{XML_PREFIX}sdt":
                child_tags: list[Element] = element.getchildren()
                is_correct_tag = False
                for grandchild_tag in child_tags:
                    if grandchild_tag.tag == f"{XML_PREFIX}sdtPr":
                        grandchild_tags: list[Element] = grandchild_tag.getchildren()
                        for grandgrandchild_tag in grandchild_tags:
                            if grandgrandchild_tag.tag == f"{XML_PREFIX}id":
                                if (
                                    grandgrandchild_tag.attrib[f"{XML_PREFIX}val"]
                                    == self.id
                                ):
                                    is_correct_tag = True
                                    break
                    elif (
                        grandchild_tag.tag == f"{XML_PREFIX}sdtContent"
                        and is_correct_tag
                    ):
                        w_p_tag: Element = grandchild_tag.getchildren()[0]
                        w_p_tag_attributes = w_p_tag.attrib

                        # Make a new <w:p> tag with the same attributes as the old one
                        new_w_p_tag: Element = etree.Element(
                            f"{XML_PREFIX}p", w_p_tag_attributes
                        )

                        # Append a <w:r> tag with a <w:t> tag inside it
                        new_w_r_tag: Element = etree.Element(f"{XML_PREFIX}r")
                        new_w_t_tag: Element = etree.Element(f"{XML_PREFIX}t")
                        new_w_t_tag.text = new_text
                        new_w_r_tag.append(new_w_t_tag)
                        new_w_p_tag.append(new_w_r_tag)

                        # Replace the old <w:p> tag with the new one
                        grandchild_tag.replace(w_p_tag, new_w_p_tag)

        # Write the new document to raw_xml
        Raw_XML.raw_xml = etree.tostring(root)
