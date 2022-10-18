# Package Imports
from datetime import datetime
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


class DatePickerContentControl(DocxContentControl):
    """
    This class contains all properties and methods for a DatePicker content control.

    :param DocxContentControl: This class extends the DocxContentControl class
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        (
            full_date,
            date_format,
            language_id,
            calendar_type,
        ) = self.__get_date_picker_information()
        self.full_date = full_date
        self.date_format = date_format
        self.language_id = language_id
        self.calendar_type = calendar_type

    def __get_date_picker_information(
        self,
    ) -> tuple[str | None, str | None, str | None, str | None]:
        """
        This method gets the date picker information of a DatePicker content control.
        The information is returned as a tuple in the following order:
        (full_date, date_format, date, time)

        :return: The date picker information of the DatePicker content control.
        :rtype: tuple[str | None, str | None, str | None, str | None]
        """

        # Return values
        full_date: str | None = None
        date_format: str | None = None
        language_id: str | None = None
        calendar_type: str | None = None

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
                    # Get the full date
                    match: Element
                    for match in element.iter(f"{XML_PREFIX}date"):
                        full_date = match.get(f"{XML_PREFIX}fullDate")

                    # Get the date format
                    for match in element.iter(f"{XML_PREFIX}dateFormat"):
                        date_format = match.get(f"{XML_PREFIX}val")

                    # Get the language id
                    for match in element.iter(f"{XML_PREFIX}lid"):
                        language_id = match.get(f"{XML_PREFIX}val")

                    # Get the calendar type
                    for match in element.iter(f"{XML_PREFIX}calendar"):
                        calendar_type = match.get(f"{XML_PREFIX}val")

        # If the date was not found
        return (full_date, date_format, language_id, calendar_type)

    def set_date(self, new_date: datetime, desired_format: str) -> None:
        """
        This method sets the date of a DatePicker content control using a datetime object.
        The format of the date is determined by the date_format property.
        Make sure to supply a valid format string that strftime can use.

        :param new_date: The new date to set.
        :type new_date: datetime
        :param desired_format: The desired format of the date.
        :type desired_format: str
        """

        # set time to 0 to avoid issues with timezones, then format
        date_to_display = new_date.replace(hour=0, minute=0, second=0, microsecond=0)

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
                    # Set the full date
                    match: Element
                    for match in element.iter(f"{XML_PREFIX}date"):
                        match.set(
                            f"{XML_PREFIX}fullDate",
                            date_to_display.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        )

                    # Set the text
                    content_tag: Element = element.find(f"{XML_PREFIX}sdtContent")

                    p_tag: Element = content_tag.getchildren()[0]
                    p_tag_attributes = p_tag.attrib

                    # Make a new <w:p> tag with the same attributes as the old one
                    new_w_p_tag: Element = etree.Element(
                        f"{XML_PREFIX}p", p_tag_attributes
                    )

                    # Append a <w:r> tag with a <w:t> tag inside it
                    new_w_r_tag: Element = etree.Element(f"{XML_PREFIX}r")
                    new_w_t_tag: Element = etree.Element(f"{XML_PREFIX}t")
                    new_w_t_tag.text = date_to_display.strftime(desired_format)
                    new_w_r_tag.append(new_w_t_tag)
                    new_w_p_tag.append(new_w_r_tag)

                    # Replace the old <w:p> tag with the new one
                    content_tag.replace(p_tag, new_w_p_tag)

        # Update the raw xml
        Raw_XML.raw_xml = etree.tostring(root, encoding="unicode")
