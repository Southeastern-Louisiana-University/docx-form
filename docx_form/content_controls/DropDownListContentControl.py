# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class DropDownListContentControl(DocxContentControl):
    def __init__(self, root: Element):
        super().__init__(root)
