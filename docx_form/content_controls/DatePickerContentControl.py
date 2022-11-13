# Package Imports
from datetime import datetime
from lxml import etree

# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
    from constants import XML_PREFIX
    from globals import Raw_XML
    from enums import DateFormats, DateFormatConversions
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX
    from ..globals import Raw_XML
    from ..enums import DateFormats, DateFormatConversions


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
    ) -> tuple[str | None, DateFormats | None, str | None, str | None]:
        """
        This method gets the date picker information of a DatePicker content control.
        The information is returned as a tuple in the following order:
        (full_date, date_format, date, time)

        :return: The date picker information of the DatePicker content control.
        :rtype: tuple[str | None, DateFormats | None, str | None, str | None]
        """

        # Return values
        full_date: str | None = None
        date_format: DateFormats | None = None
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
                        date_format = self.__convert_date_to_date_format(
                            match.get(f"{XML_PREFIX}val")
                        )

                    # Get the language id
                    for match in element.iter(f"{XML_PREFIX}lid"):
                        language_id = match.get(f"{XML_PREFIX}val")

                    # Get the calendar type
                    for match in element.iter(f"{XML_PREFIX}calendar"):
                        calendar_type = match.get(f"{XML_PREFIX}val")

        # If the date was not found
        return (full_date, date_format, language_id, calendar_type)

    def __convert_date_to_date_format(self, date: str) -> DateFormats | None:
        """
        This method converts a date from a .docx file to a DateFormats enum.

        :param str date: The date to convert
        :return: The date format
        :rtype: DateFormats | None
        """

        # Date conversions are listed in order as they appear in date_formats.py
        if date == "M/d/yyyy":
            return DateFormats.M_d_yyyy_SLASHED
        elif date == "dddd, MMMM d, yyyy":
            return DateFormats.dddd_MMMM_d_yyyy
        elif date == "MMMM d, yyyy":
            return DateFormats.MMMM_d_yyyy
        elif date == "M/d/yy":
            return DateFormats.M_d_yy
        elif date == "yyyy-MM-dd":
            return DateFormats.yyyy_MM_dd
        elif date == "d-MMM-yy":
            return DateFormats.d_MMM_yy
        elif date == "M.d.yyyy":
            return DateFormats.M_d_yyyy_DOTTED
        elif date == "MMM. d, yy":
            return DateFormats.MMM_d_yy
        elif date == "d MMMM yyyy":
            return DateFormats.d_MMMM_yyyy
        elif date == "MMMM yy":
            return DateFormats.MMMM_yy
        elif date == "MMM-yy":
            return DateFormats.MMM_yy
        elif date == "M/d/yyyy h:mm am/pm":
            return DateFormats.M_d_yyyy_h_mm_am_pm
        elif date == "M/d/yyyy h:mm:ss am/pm":
            return DateFormats.M_d_yyyy_h_mm_ss_am_pm
        elif date == "h:mm am/pm":
            return DateFormats.h_mm_am_pm
        elif date == "h:mm:ss am/pm":
            return DateFormats.h_mm_ss_am_pm
        elif date == "HH:mm":
            return DateFormats.HH_mm
        elif date == "HH:mm:ss":
            return DateFormats.HH_mm_ss

        return None

    def __get_date_format_conversion(self) -> DateFormatConversions | None:
        """
        This method returns the conversion of the date format.

        :return: The conversion of the date format.
        :rtype: DateFormatConversions | None
        """

        match self.date_format:
            case DateFormats.M_d_yyyy_SLASHED:
                return DateFormatConversions.M_d_yyyy_SLASHED
            case DateFormats.dddd_MMMM_d_yyyy:
                return DateFormatConversions.dddd_MMMM_d_yyyy
            case DateFormats.MMMM_d_yyyy:
                return DateFormatConversions.MMMM_d_yyyy
            case DateFormats.M_d_yy:
                return DateFormatConversions.M_d_yy
            case DateFormats.yyyy_MM_dd:
                return DateFormatConversions.yyyy_MM_dd
            case DateFormats.d_MMM_yy:
                return DateFormatConversions.d_MMM_yy
            case DateFormats.M_d_yyyy_DOTTED:
                return DateFormatConversions.M_d_yyyy_DOTTED
            case DateFormats.MMM_d_yy:
                return DateFormatConversions.MMM_d_yy
            case DateFormats.d_MMMM_yyyy:
                return DateFormatConversions.d_MMMM_yyyy
            case DateFormats.MMMM_yy:
                return DateFormatConversions.MMMM_yy
            case DateFormats.MMM_yy:
                return DateFormatConversions.MMM_yy
            case DateFormats.M_d_yyyy_h_mm_am_pm:
                return DateFormatConversions.M_d_yyyy_h_mm_am_pm
            case DateFormats.M_d_yyyy_h_mm_ss_am_pm:
                return DateFormatConversions.M_d_yyyy_h_mm_ss_am_pm
            case DateFormats.h_mm_am_pm:
                return DateFormatConversions.h_mm_am_pm
            case DateFormats.h_mm_ss_am_pm:
                return DateFormatConversions.h_mm_ss_am_pm
            case DateFormats.HH_mm:
                return DateFormatConversions.HH_mm
            case DateFormats.HH_mm_ss:
                return DateFormatConversions.HH_mm_ss

        return None

    def set_date(self, new_date: datetime) -> None:
        """
        This method sets the date of a DatePicker content control using a datetime object.
        The format of the date is determined by the date_format property.
        Make sure to supply a valid format string that strftime can use.

        :param new_date: The new date to set.
        :type new_date: datetime

        :return None: None
        """

        desired_format = self.__get_date_format_conversion()

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
                            new_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
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
                    new_w_t_tag.text = new_date.strftime(desired_format)
                    new_w_r_tag.append(new_w_t_tag)
                    new_w_p_tag.append(new_w_r_tag)

                    # Replace the old <w:p> tag with the new one
                    content_tag.replace(p_tag, new_w_p_tag)

        # Update class variable
        self.full_date = new_date
        self.text = new_date.strftime(desired_format)

        # Update the raw xml
        Raw_XML.raw_xml = etree.tostring(root, encoding="unicode")
