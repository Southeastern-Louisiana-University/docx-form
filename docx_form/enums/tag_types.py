from enum import Enum


class TagType(Enum):
    """
    This enum contains the two types of parent tags that the package is looking for.

    :param Enum: This is the generic Enum class from the enum module
    """

    SDT = "sdt"
    P = "p"
