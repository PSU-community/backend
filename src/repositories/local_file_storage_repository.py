from hashlib import sha1

import aiofiles
from fastapi import UploadFile

from src.settings import settings


class LocalFileStorageRepository:
    @staticmethod
    async def upload_file(file: UploadFile) -> str:
        file_ext = file.filename.split(".")[-1]
        filesha = sha1(file.filename.encode()).hexdigest()
        path = settings.FILES_DIR / f"{filesha}.{file_ext}"
        async with aiofiles.open(path, mode="wb") as filehandle:
            await filehandle.write(await file.read())

        return f"{filesha}.{file_ext}"

    @staticmethod
    async def delete_file(filename: str):
        ...

    @staticmethod
    async def get_file_path(file: str) -> str:
        return f"D:\\files\\{file}"
