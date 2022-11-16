from enum import Enum


class DateFormats(str, Enum):
    """
    This enum contains the default date formats supported by .docx files.

    :param Enum: This is the generic Enum class from the enum module
    """

    M_d_yyyy_SLASHED = "M/d/yyyy"
    dddd_MMMM_d_yyyy = "dddd, MMMM d, yyyy"
    MMMM_d_yyyy = "MMMM d, yyyy"
    M_d_yy = "M/d/yy"
    yyyy_MM_dd = "yyyy-MM-dd"
    d_MMM_yy = "d-MMM-yy"
    M_d_yyyy_DOTTED = "M.d.yyyy"
    MMM_d_yy = "MMM. d, yy"
    d_MMMM_yyyy = "d MMMM yyyy"
    MMMM_yy = "MMMM yy"
    MMM_yy = "MMM-yy"
    M_d_yyyy_h_mm_am_pm = "M/d/yyyy h:mm am/pm"
    M_d_yyyy_h_mm_ss_am_pm = "M/d/yyyy h:mm:ss am/pm"
    h_mm_am_pm = "h:mm am/pm"
    h_mm_ss_am_pm = "h:mm:ss am/pm"
    HH_mm = "HH:mm"
    HH_mm_ss = "HH:mm:ss"
