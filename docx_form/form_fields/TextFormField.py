# Local Imports
from .DocxFormField import DocxFormField

try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element


class TextFormField(DocxFormField):
    """
    This class holds all information & functions regarding a text form field.
    """

    def __init__(self, root: Element, file_path: str, name: str) -> None:
        super.__init__(root, file_path, name)
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
