from ..models.tables.tables import SectionTable, SectionThemesTable, InformationalContentTable, PersonalInformationTable
from ..utils.repository import SQLAlchemyRepository


class SectionRepository(SQLAlchemyRepository):
    table_model = SectionTable


class SectionThemeRepository(SQLAlchemyRepository):
    table_model = SectionThemesTable


class InformationalContentRepository(SQLAlchemyRepository):
    table_model = InformationalContentTable


class PersonalInformationRepository(SQLAlchemyRepository):
    table_model = PersonalInformationTable


class ContentRepository:
    def __init__(self):
        self.section = SectionRepository()
        self.section_theme = SectionThemeRepository()
        self.informational_content = InformationalContentRepository()
        self.personal_information = PersonalInformationRepository()
