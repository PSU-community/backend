from abc import abstractmethod
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_128 = Annotated[str, 128]


class BaseTable(DeclarativeBase):
    type_annotation_map = {
        str_128: String(128)
    }

    @abstractmethod
    def to_schema_model(self):
        raise NotImplementedError

