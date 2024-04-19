from enum import Enum, IntFlag


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


class PersonalInformationTypes(str, Enum):
    BOOKMARK = "BOOKMARK"
    NOTE = "NOTE"


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0
