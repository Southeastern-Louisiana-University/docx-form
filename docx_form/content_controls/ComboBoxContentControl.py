# Local Imports
from .OptionalContentControl import OptionalContentControl

try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class ComboBoxContentControl(OptionalContentControl):
    """
    This class contains all properties and methods for a ComboBox content control.

    :param OptionalContentControl: This class extends the OptionalContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
