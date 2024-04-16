from typing import Any, Optional

from ..models.search import Document
from ..search.client import index
from ..utils.search_repository import SearchRepository


class MeiliSearchRepository(SearchRepository):
    @staticmethod
    def add_document(document: Document):
        index.add_documents(document)

    @staticmethod
    def update_document(updated_document: Document):
        index.update_documents([updated_document])

    @staticmethod
    def delete_document(document_id: int):
        index.delete_document(document_id)

    @staticmethod
    def search(query: str, params: Optional[dict[str, Any]] = None) -> list[Document]:
        default_params = {
            "attributesToCrop": ["content"],
            "attributesToHighlight": ["title", "content"],
            "cropLength": 7,
        }
        if params is not None:
            default_params.update(**params)

        result = index.search(query, params)

        hits_map = map(
            lambda hit_doc: hit_doc.get("_formatted") or hit_doc, result["hits"]
        )
        return list(hits_map)

    @staticmethod
    def search_in_documents(document_ids: list[int], query: str):
        docs_str = ",".join(map(lambda i: str(i), document_ids))
        return MeiliSearchRepository.search(query, {"filter": [f"id IN [{docs_str}]"]})
