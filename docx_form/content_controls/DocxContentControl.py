try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element


class DocxContentControl:
    """
    This is the parent class of all supported content controls.
    It is responsible for getting the id and text of the content control.
    """

    def __init__(self, root: Element, file_path: str):
        self.root = root
        self.file_path = file_path
        self.id = self.__get_id()
        self.text = self.__get_text()

    def __get_id(self) -> str:
        """
        Return the value of the id tag
        """
        child: Element
        for child in self.root.iter(f"{XML_PREFIX}id"):
            return child.attrib[f"{XML_PREFIX}val"]

        # TODO: Raise an error if the id is not found
        return "NOT FOUND"

    def __get_text(self) -> str:
        """
        Return the value of each text tag concatenated
        """
        child: Element
        tag_text: str = ""
        for child in self.root.iter(f"{XML_PREFIX}t"):
            tag_text += child.text

        return tag_text
