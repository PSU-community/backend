from typing import Optional

from .base import IdSchema
from .create import (
    InformationalContentCreate,
    PersonalInformationCreate,
    SectionCreate,
    SectionThemeCreate,
)


class SectionSchema(IdSchema, SectionCreate):
    themes: list["SectionThemeSchema"]


class SectionThemeSchema(IdSchema, SectionThemeCreate): ...


class InformationalContentSchema(IdSchema, InformationalContentCreate):
    file_url: Optional[str]


class PersonalInformationSchema(IdSchema, PersonalInformationCreate): ...
