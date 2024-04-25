from abc import ABC, abstractmethod

from fastapi import UploadFile


class FileStorageRepository(ABC):
    @abstractmethod
    @staticmethod
    async def upload_file(file: UploadFile) -> str:
        raise NotImplementedError

    @abstractmethod
    @staticmethod
    async def get_file_path(file: str) -> str:
        raise NotImplementedError
