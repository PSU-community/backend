from ..models.tables.users import UserTable
from ..utils.db_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    table_model = UserTable
