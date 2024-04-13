from abc import ABC, abstractmethod


class SearchRepository(ABC):
    @staticmethod
    @abstractmethod
    def add_document(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_document(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete_document(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def search(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def search_in_documents(self):
        raise NotImplementedError
