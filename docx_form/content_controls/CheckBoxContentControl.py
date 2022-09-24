# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class CheckBoxContentControl(DocxContentControl):
    """
    This class contains the properties and functions associated with the Check Box content control.

    :param DocxContentControl: This class extends DocxContentControl
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.type = "CheckBox Content Control"
