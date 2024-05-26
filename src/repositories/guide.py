from src.models.tables.tables import GuideTable
from src.utils.abstract.db_repository import SQLAlchemyRepository


class GuideRepository(SQLAlchemyRepository):
    table_model = GuideTable
