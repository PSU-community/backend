from fastapi import APIRouter, HTTPException, UploadFile
import pypandoc
from starlette import status

from src.api.dependencies import IAdminUser
from src.repositories.local_file_storage_repository import LocalFileStorageRepository
from src.settings import settings

router = APIRouter()


@router.post("/transform")
async def transform_text_file(file: UploadFile, user: IAdminUser):
    file_format = file.filename.split('.')[-1]
    if file_format not in {"docx", "doc", "txt"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only txt, doc and docx are supported"
        )

    if file_format == "txt":
        text = await file.read()
        return text.decode("utf-8")

    filename = await LocalFileStorageRepository.upload_file(file)
    file_path = settings.FILES_DIR / filename
    markdown_text = pypandoc.convert_file(file_path, format="docx", to="gfm")
    return markdown_text
