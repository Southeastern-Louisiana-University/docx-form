from enum import Enum


class DateFormatConversions(str, Enum):
    """
    This enum contains the date format conversions to strftime from the default date formats supported by .docx files.

    :param Enum: This is the generic Enum class from the enum module
    """

    M_d_yyyy_SLASHED = "%m/%d/%Y"
    dddd_MMMM_d_yyyy = "%A, %B %d, %Y"
    MMMM_d_yyyy = "%B %d, %Y"
    M_d_yy = "%m/%d/%y"
    yyyy_MM_dd = "%Y-%m-%d"
    d_MMM_yy = "%d-%b-%y"
    M_d_yyyy_DOTTED = "%m.%d.%Y"
    MMM_d_yy = "%b. %d, %y"
    d_MMMM_yyyy = "%d %B %Y"
    MMMM_yy = "%B %y"
    MMM_yy = "%b-%y"
    M_d_yyyy_h_mm_am_pm = "%m/%d/%Y %I:%M %p"
    M_d_yyyy_h_mm_ss_am_pm = "%m/%d/%Y %I:%M:%S %p"
    h_mm_am_pm = "%I:%M %p"
    h_mm_ss_am_pm = "%I:%M:%S %p"
    HH_mm = "%H:%M"
    HH_mm_ss = "%H:%M:%S"
