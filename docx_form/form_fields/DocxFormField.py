try:
    from type_aliases import Element
except ImportError:
    from ..type_aliases import Element


class DocxFormField:
    """
    This is the parent class for all supported form fields.
    """

    def __init__(self, root: Element, file_path: str, name: str) -> None:
        self.root = root
        self.file_path = file_path
        self.name = name
