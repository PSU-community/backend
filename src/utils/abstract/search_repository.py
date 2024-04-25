from abc import ABC, abstractmethod
from typing import Any, Optional

from src.models.search import Document


class SearchRepository(ABC):
    @staticmethod
    @abstractmethod
    def add_document(document: Document):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_document(updated_document: Document):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete_document(document_id: int):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def search(query: str, params: Optional[dict[str, Any]] = None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def search_in_documents(document_ids: list[int], query: str):
        raise NotImplementedError
