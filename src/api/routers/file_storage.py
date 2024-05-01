from typing import Optional

from fastapi import Depends, Form, UploadFile, APIRouter
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer

from src.api.dependencies import IAdminUser, IContentService
from src.models.schemas.content import MediaFileSchema
from src.models.schemas.create import CreateMediaSchema, RequestMediaSchema
from src.repositories.local_file_storage_repository import LocalFileStorageRepository

router = APIRouter(dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.post("/media")
async def upload_media_file(
    service: IContentService,
    user: IAdminUser,
    file: Optional[UploadFile] = None,
    payload_json: RequestMediaSchema = Form(),
) -> MediaFileSchema:
    create_media = CreateMediaSchema(**payload_json.model_dump())

    if file is not None:
        filename = await LocalFileStorageRepository.upload_file(file)
        create_media.url = filename

    return await service.add_media_file(create_media)


@router.get("/media/list")
async def get_media_list(user: IAdminUser, service: IContentService) -> list[MediaFileSchema]:
    return await service.get_media_file_list()

#
# @router.get("/media/{name}")
# async def get_file(name: str):
#     return FileResponse(await LocalFileStorageRepository.get_file_path(name))
