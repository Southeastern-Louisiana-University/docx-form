# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class DropDownListContentControl(DocxContentControl):
    """
    This class contains all properties and methods for a Drop-Down List content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.type = "DropDown Content Control"
        
