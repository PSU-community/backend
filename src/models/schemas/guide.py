from pydantic import BaseModel


class GuideSchema(BaseModel):
    id: int
    name: str
    content: str
