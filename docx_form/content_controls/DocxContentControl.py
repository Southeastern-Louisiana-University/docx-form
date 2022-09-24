# Local Imports
try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element


class DocxContentControl:
    """
    This is the parent class of all content controls.
    It is responsible for getting the id and text of the content control.
    """

    def __init__(self, root: Element, file_path: str):
        self.root = root
        self.file_path = file_path
        self.id = self.__get_id()
        self.text = self.__get_text()

    # Note: May need to account for the id not being the first child
    def __get_id(self) -> str:
        root_children: list[Element] = self.root.getchildren()
        id_element: Element = root_children[0].getchildren()[0]
        return id_element.attrib[f"{XML_PREFIX}val"]

    def __get_text(self) -> str:
        root_children: list[Element] = self.root.getchildren()

        # Find the <w:sdtContent> tag
        sdt_content_tag: Element
        for child in root_children:
            if "sdtContent" in child.tag:
                sdt_content_tag = child
                break

        # <w:sdtContent> to <w:p>
        text_container: list[Element] = sdt_content_tag.getchildren()[0]

        # If the tag is a <w:r> tag, then it is a CheckBoxContentControl
        text: str = ""
        if text_container.tag == f"{XML_PREFIX}r":
            # Find the <w:t> tag
            w_t_tag: Element
            child_tag: Element
            for child_tag in text_container.getchildren():
                if f"{XML_PREFIX}t" == child_tag.tag:
                    w_t_tag = child_tag
                    break

            # Append the text
            text += w_t_tag.text
        # If it is not a CheckBoxContentControl
        else:
            text_container = text_container.getchildren()
            # For each <w:r> tag, get the text in the <w:t> tag
            for tag in text_container:
                # Find the <w:t> tag
                w_t_tag: Element
                for child_tag in tag.getchildren():
                    if f"{XML_PREFIX}t" == child_tag.tag:
                        w_t_tag = child_tag
                        break

                # Append the text
                text += w_t_tag.text

        return text
