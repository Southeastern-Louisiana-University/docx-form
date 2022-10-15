# Local Imports
from .DocxFormField import DocxFormField

try:
    from constants import XML_PREFIX
    from type_aliases import Element
except ImportError:
    from ..constants import XML_PREFIX
    from ..type_aliases import Element

# TODO: Need to look at this a bit more before exposing to user
class CheckBoxFormField(DocxFormField):
    """
    This class holds all information & functions regarding a check box form field.
    """

    def __init__(self, root: Element, file_path: str, name: str) -> None:
        super.__init__(root, file_path, name)
        self.value = self.__get_is_checked()

    def __get_is_checked(self) -> str:
        """
        Return the value of each text tag concatenated
        """
        child: Element
        for child in self.root.iter(f"{XML_PREFIX}ffData"):
            # If > 1 checkbox in a <w:p> tag, we need to find the correct one
            name_tag: Element = child.find(f"{XML_PREFIX}name")
            name_tag_value: str = name_tag.attrib[f"{XML_PREFIX}val"]
            if name_tag_value == self.name:
                for match in child.iter(f"{XML_PREFIX}checked"):
                    return "checked"

        return "unchecked"
