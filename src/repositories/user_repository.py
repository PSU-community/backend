from ..models.tables.tables import UserTable
from ..utils.db_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    table_model = UserTable
