# Local Imports
from .TextualContentControl import TextualContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class PlainTextContentControl(TextualContentControl):
    """
    This class contains all properties and methods for a Plain Text content control.

    :param TextualContentControl: This class extends the TextualContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
