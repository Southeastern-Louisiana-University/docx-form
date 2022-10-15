try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element


class TextFormField:
    """
    This class holds all information & functions regarding a text form field.
    """

    def __init__(self, root: Element, file_path: str, name: str) -> None:
        self.root = root
        self.file_path = file_path
        self.name = name
        self.value = self.__get_text()

    def __get_text(self) -> str:
        """
        Return the value of each text tag concatenated
        """
        child: Element
        tag_text: str = ""
        for child in self.root.iter(f"{XML_PREFIX}t"):
            tag_text += child.text

        return tag_text
