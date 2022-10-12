from enum import Enum


class InstrTextOptions(str, Enum):
    """
    This enum contains the three supported values of the <w:instrText> tag. This tag is only used in
    legacy Form Fields.

    :param Enum: This is the generic Enum class from the enum module
    """

    FORM_DROPDOWN = " FORMDROPDOWN "
    FORM_TEXT = " FORMTEXT "
    FORM_CHECKBOX = " FORMCHECKBOX "
