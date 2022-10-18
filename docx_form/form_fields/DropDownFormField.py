# Local Imports
from .DocxFormField import DocxFormField

try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element


class DropDownFormField(DocxFormField):
    """
    This class holds all information & functions regarding a drop down form field.
    """

    def __init__(self, root: Element, file_path: str, name: str) -> None:
        super.__init__(root, file_path, name)
        self.value = "Not currently supported"
        self.entries = self.__get_entries()

    def __get_entries(self) -> list[str]:
        """
        Return the value of each listEntry tag's val attribute
        """
        entries: list[str] = []
        child: Element
        for child in self.root.iter(f"{XML_PREFIX}listEntry"):
            entries.append(child.attrib[f"{XML_PREFIX}val"])

        return entries
