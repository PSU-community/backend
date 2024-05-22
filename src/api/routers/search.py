from fastapi import APIRouter

from src.api.dependencies import IContentService

router = APIRouter(tags=["Контент::Поиск"])


@router.get("/search")
async def search_post(query: str, service: IContentService):
    return service.search_posts(query)
