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

    def set_text(self, new_text: str) -> None:
        """
        This method sets the text of a Plain Text content control.

        :param str new_text: The new text to set
        """

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
                    # Replace the text
                    content_tag: Element = element.find(f"{XML_PREFIX}sdtContent")

                    # TODO: Test this in case it is not a universal index
                    p_tag: Element = content_tag.getchildren()[0]
                    p_tag_attributes = p_tag.attrib

                    # Make a new <w:p> tag with the same attributes as the old one
                    new_w_p_tag: Element = etree.Element(
                        f"{XML_PREFIX}p", p_tag_attributes
                    )

                    # Append a <w:r> tag with a <w:t> tag inside it
                    new_w_r_tag: Element = etree.Element(f"{XML_PREFIX}r")
                    new_w_t_tag: Element = etree.Element(f"{XML_PREFIX}t")
                    new_w_t_tag.text = new_text
                    new_w_r_tag.append(new_w_t_tag)
                    new_w_p_tag.append(new_w_r_tag)

                    # Replace the old <w:p> tag with the new one
                    content_tag.replace(p_tag, new_w_p_tag)

        # Write the new document to raw_xml
        Raw_XML.raw_xml = etree.tostring(root)
