# Package Imports
from lxml import etree

# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
    from constants import XML_PREFIX
    from globals import Raw_XML
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX
    from ..globals import Raw_XML


class ComboBoxOption:
    """
    This class contains all properties and methods for a ComboBox list item.

    :param str display_text: The display text of the option
    :param str value: The value of the option
    """

    def __init__(self, display_text: str, value: str):
        self.display_text = display_text
        self.value = value


class ComboBoxContentControl(DocxContentControl):
    """
    This class contains all properties and methods for a ComboBox content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.options = self.__get_options()

    def __get_options(self) -> list[ComboBoxOption] | None:
        """
        This method gets the options of a ComboBox content control.

        :return: The options of the ComboBox content control
        :rtype: list[ComboBoxOption] | None
        """
        # The root of the document
        root: Element = etree.XML(Raw_XML.raw_xml)
        # The body of the document
        body: Element = root.getchildren()[0]

        element: Element
        for element in body.iter(f"{XML_PREFIX}sdt"):
            # Get the nested id tag
            id_tag: Element
            for id_tag in element.iter(f"{XML_PREFIX}id"):
                # If the id matches
                if id_tag.get(f"{XML_PREFIX}val") == self.id:
                    # Get the options
                    options: list[ComboBoxOption] = []
                    option: Element
                    for option in element.iter(f"{XML_PREFIX}listItem"):
                        tag_info = ComboBoxOption(
                            option.get(f"{XML_PREFIX}displayText"),
                            option.get(f"{XML_PREFIX}value"),
                        )
                        options.append(tag_info)

                    return options

        return None

    def print_options(self) -> None:
        """
        This method prints the options of a ComboBox content control.
        """
        if self.options is not None:
            index = 0
            for option in self.options:
                print(
                    f'{index}: Display Value = "{option.display_text}" || Value = "{option.value}"'
                )
                index += 1
        else:
            print("No options found")

    def set_text(self, option_index: int) -> None:
        """
        This method sets the text of a ComboBox content control.

        :param int option_index: The index of the new text to set
        """

        # The root of the document
        root: Element = etree.XML(Raw_XML.raw_xml)
        # The body of the document
        body: Element = root.getchildren()[0]

        element: Element
        for element in body.iter(f"{XML_PREFIX}sdt"):
            # Get the nested id tag
            id_tag: Element
            for id_tag in element.iter(f"{XML_PREFIX}id"):
                # If the id matches
                if id_tag.get(f"{XML_PREFIX}val") == self.id:
                    # Replace the text
                    content_tag: Element = element.find(f"{XML_PREFIX}sdtContent")

                    # TODO: Test this in case it is not a universal index
                    # Dig to the t tag
                    p_tag: Element = content_tag.getchildren()[0]
                    r_tag: Element = p_tag.getchildren()[0]
                    t_tag: Element = r_tag.getchildren()[0]

                    # Replace the old text with the new option
                    t_tag.text = self.options[option_index].value

        # Write the new document to raw_xml
        Raw_XML.raw_xml = etree.tostring(root)
