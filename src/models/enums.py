from enum import Enum, IntFlag, IntEnum


class ContentTypes(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    PRESENTATION = "PRESENTATION"
    TABLE = "TABLE"
    TEST = "TEST"
    DIAGRAM = "DIAGRAM"
    PDF = "PDF"


class MediaTypes(IntEnum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    PRESENTATION = 4
    PDF = 5
    TEST = 6
    FILE = 7


class PersonalInformationTypes(str, Enum):
    BOOKMARK = "BOOKMARK"
    NOTE = "NOTE"


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0
