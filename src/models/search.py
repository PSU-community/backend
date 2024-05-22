from typing import Optional, TypedDict


class Document(TypedDict):
    id: int
    category_id: int
    subcategory_id: Optional[int] = None
    content: str
