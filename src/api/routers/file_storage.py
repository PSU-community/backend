import json
from typing import Optional

from fastapi import Form, UploadFile, APIRouter
from fastapi.responses import FileResponse

from src.api.dependencies import IAdminUser, IContentService
from src.models.enums import MediaTypes
from src.models.schemas.content import MediaFileSchema
from src.models.schemas.create import CreateMediaSchema
from src.models.schemas.update import MediaUpdate
from src.repositories.local_file_storage_repository import LocalFileStorageRepository

router = APIRouter()


@router.get("/media/{media_id}")
async def get_media(media_id: int, service: IContentService) -> MediaFileSchema:
    return await service.get_media(media_id)


@router.post("/media")
async def upload_media(
    service: IContentService,
    user: IAdminUser,
    file: Optional[UploadFile] = Form(None),
    json_payload: Optional[str] = Form(None),
) -> MediaFileSchema:
    create_media = CreateMediaSchema(**json.loads(json_payload))
    if create_media.data:
        create_media.data = json.dumps(create_media.data)

    if file is not None:
        hashed_filename = await LocalFileStorageRepository.upload_file(file)
        create_media.file_url = f"/media/{hashed_filename}"
        names = file.filename.split(".")
        names.pop()
        create_media.file_name = ".".join(names)

    return await service.add_media_file(create_media)


@router.get("/media/list")
async def get_media_list(user: IAdminUser, service: IContentService) -> list[MediaFileSchema]:
    return await service.get_media_file_list()


@router.get("/media/list/{media_type}")
async def get_media_list_with_type(
    media_type: MediaTypes,
    user: IAdminUser,
    service: IContentService
) -> list[MediaFileSchema]:
    return await service.get_media_file_list(type=media_type)


@router.patch("/media/{media_id}")
async def update_media(media_id: int, media_update: MediaUpdate, service: IContentService):
    media_update.data = json.dumps(media_update.data)
    return await service.update_media(media_id, media_update)


@router.get("/media/name/{name}")
async def get_file(name: str):
    return FileResponse(await LocalFileStorageRepository.get_file_path(name))
