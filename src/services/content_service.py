from typing import Optional, overload

from src.api import exceptions
from src.models.enums import MediaTypes, PersonalInformationTypes
from src.models.schemas.content import (
    CategorySchema,
    MediaFileSchema,
    PersonalInformationSchema, SubCategorySchema,
    PostSchema,
)
from src.models.schemas.create import (
    CreateMediaSchema, PersonalInformationCreate, PostCreate,
    CategoryCreate,
    SubCategoryCreate,
)
from src.models.schemas.update import UserContentUpdate, MediaUpdate, PostUpdate, SubCategoryUpdate, CategoryUpdate
from src.models.tables.tables import CategoryTable, PostTable
from src.repositories.content_repository import ContentRepository
from src.repositories.meili_search_repository import MeiliSearchRepository


class ContentService:
    def __init__(self):
        self.repository = ContentRepository()
        self.search = MeiliSearchRepository

    async def get_category(
        self, category_id: int
    ) -> CategorySchema:
        return await self.repository.category.get_by_id(category_id)

    async def get_category_list(
        self,
    ) -> list[CategorySchema]:
        return await self.repository.get_categories()

    async def add_category(self, category_create: CategoryCreate):
        category: CategorySchema = await self.repository.category.add_one(
            category_create.model_dump(exclude={"subcategories"})
        )
        # TODO: make with one session
        for subcategory in category_create.subcategories:
            await self.repository.subcategory.add_one(
                {"category_id": category.id, "name": subcategory}
            )

    async def update_category(self, category_id: int, category_update: CategoryUpdate):
        await self.repository.category.update_by_id(
            category_id, category_update.model_dump(exclude_none=True)
        )

    async def delete_category(self, category: CategorySchema):
        await self.repository.category.remove_by_id(category.id)
        if category.post:
            self.search.delete_document(category.post.id)

    async def get_subcategory(self, subcategory_id: int) -> SubCategorySchema:
        return await self.repository.subcategory.get_by_id(subcategory_id)

    async def add_subcategory(
        self, subcategory_create: SubCategoryCreate
    ) -> SubCategorySchema:
        subcategory: SubCategorySchema = await self.repository.subcategory.add_one(
            subcategory_create.model_dump()
        )
        post: PostSchema = await self.repository.post.get_one(category_id=subcategory.category_id)
        if not post or post.subcategory_id is not None:
            return subcategory
        await self.repository.post.update_by_id(post.id, {"subcategory_id": subcategory.id})
        self.search.update_document({"id": post.id, "subcategory_id": subcategory.id})

        return subcategory

    async def update_subcategory(
        self, subcategory_id: int, theme_update: SubCategoryUpdate
    ):
        await self.repository.subcategory.update_by_id(
            subcategory_id, theme_update.model_dump(exclude_none=True)
        )

    async def delete_subcategory(self, subcategory: SubCategorySchema):
        await self.repository.subcategory.remove_by_id(subcategory.id)
        if subcategory.post is not None:
            self.search.delete_document(subcategory.post.id)

    async def get_posts(self) -> list[PostSchema]:
        return await self.repository.post.get_all()

    async def get_post(
        self,
        *,
        post_id:  Optional[int] = None,
        category_id:  Optional[int] = None,
        subcategory_id: Optional[int] = None,
        should_increment_count: bool = True,
        fetch_all: bool = False
    ) -> PostSchema:
        if post_id is None and category_id is None and subcategory_id is None:
            raise exceptions.missing_arguments

        post: PostSchema
        # if fetch_all:
        #     post = await self.repository.post.get_post_with_full_nested_data(id=post_id, category_id=category_id, subcategory_id=subcategory_id)
        # else:
        post = await self.repository.post.get_one(
            id=post_id, category_id=category_id, subcategory_id=subcategory_id
        )

        if post is not None and should_increment_count:
            print("INCREMENT", post.views)
            # TODO: implement with one session
            await self.repository.post.update_by_id(post.id, {"views": post.views + 1})
        return post

    async def add_post(self, post_create: PostCreate):
        post = await self.repository.post.add_one(post_create.model_dump())
        self.search.add_document({
            "id": post.id, 
            "content": post.content, 
            "category_id": post.category_id, 
            "subcategory_id": post.subcategory_id,
        })

    async def update_post(self, post_id: int, post_update: PostUpdate):
        await self.repository.post.update_by_id(post_id, post_update.model_dump())
        self.search.update_document({"id": post_id, "content": post_update.content})

    async def get_popular_posts(self):
        return await self.repository.get_popular_posts()

    async def get_media_file_list(self, type: Optional[MediaTypes] = None):
        return await self.repository.media.get_many(type=type.value if type else None)

    async def get_media(self, media_id: int):
        return await self.repository.media.get_by_id(media_id)

    async def add_media_file(self, media_file: CreateMediaSchema) -> MediaFileSchema:
        return await self.repository.media.add_one(media_file.model_dump())

    async def update_media(self, media_id: int, media_update: MediaUpdate) -> MediaFileSchema:
        await self.repository.media.update_by_id(media_id, media_update.model_dump())

    async def delete_media_file(self, media_file_id: int):
        return await self.repository.media.remove_by_id(media_file_id)

    @overload
    def search_posts(self, query: str, /): ...

    @overload
    def search_posts(self, query: str, /, post_ids: list[int]): ...

    def search_posts(self, query: str, /, post_id: int = None):
        if post_id is None:
            return self.search.search(query)
        return self.search.search_in_documents([post_id], query)


    async def add_user_content(self, user_id: int, content_create: PersonalInformationCreate):
        await self.repository.personal_information.add_one({**content_create.model_dump(), "user_id": user_id})

    async def get_user_content_list(self, user_id: int):
        return await self.repository.personal_information.get_many(user_id=user_id)
    
    async def get_user_content_list_by_type(self, user_id: int, type: PersonalInformationTypes):
        return await self.repository.personal_information.get_many(user_id=user_id, content_type=type.value)
    
    async def get_user_content_list_by_post(self, user_id: int, post_id: int):
        return await self.repository.personal_information.get_many(user_id=user_id, post_id=post_id)

    async def get_user_content(self, content_id: int) -> PersonalInformationSchema:
        return await self.repository.personal_information.get_by_id(content_id)

    async def update_user_content(self, content_id: int, content_update: UserContentUpdate):
        return await self.repository.personal_information.update_by_id(content_id, content_update.model_dump())

    async def delete_user_content(self, content_id: int):
        return await self.repository.personal_information.remove_by_id(content_id)