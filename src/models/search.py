from typing import Optional, TypedDict


class Document(TypedDict):
    post_id: int
    category_id: int
    subcategory_id: Optional[int] = None
    content: str
