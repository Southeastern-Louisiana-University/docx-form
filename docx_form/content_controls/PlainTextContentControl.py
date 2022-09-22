# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class PlainTextContentControl(DocxContentControl):
    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)