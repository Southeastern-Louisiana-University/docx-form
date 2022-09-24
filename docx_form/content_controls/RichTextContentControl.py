# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class RichTextContentControl(DocxContentControl):
    """
    This class contains all properties and methods for a Rich Text content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.type = "Rich Text Content Control"
