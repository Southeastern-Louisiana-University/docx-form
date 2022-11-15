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


class Option:
    """
    This class contains all properties and methods for an optional item.

    :param str display_text: The display text of the option
    :param str value: The value of the option
    """

    def __init__(self, display_text: str, value: str):
        self.display_text = display_text
        self.value = value


class OptionalContentControl(DocxContentControl):
    """
    This class contains all properties and methods for an optional content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.options = self.__get_options()

    def __get_options(self) -> list[Option] | None:
        """
        This method gets the options of a optional content control.

        :return: The options of the optional content control
        :rtype: list[Option] | None
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
                    options: list[Option] = []
                    option = element
                    for option in element.iter(f"{XML_PREFIX}listItem"):
                        tag_info = Option(
                            option.get(f"{XML_PREFIX}displayText"),
                            option.get(f"{XML_PREFIX}value"),
                        )
                        options.append(tag_info)

                    return options

        return None

    def print_options(self) -> None:
        """
        This method prints the options of an optional content control.
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

    def set_option(self, new_option: int) -> None:
        """
        This method sets the text of an optional content control

        :param int new_option: The option to set (index from the print_options() method)
        """

        # The root of the doxument
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
                    t_tag.text = self.options[new_option].value

        # Write the new document to raw_xml
        Raw_XML.raw_xml = etree.tostring(root)
        self.text = self.options[new_option].value
