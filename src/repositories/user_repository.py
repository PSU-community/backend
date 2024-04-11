from ..models.tables.tables import UserTable
from ..utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    table_model = UserTable
