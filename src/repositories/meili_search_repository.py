from typing import Any, Optional

from ..models.search import Document
from ..search.client import index, client
from src.utils.abstract.search_repository import SearchRepository


class MeiliSearchRepository(SearchRepository):
    @staticmethod
    def update_documents(documents: list[Document]):
        index.add_documents(documents, "id")
        f = index.get_documents()
        print(f.results)

    @staticmethod
    def add_document(document: Document):
        index.add_documents(document, "id")
        print(client.get_tasks().results)

    @staticmethod
    def update_document(updated_document: Document):
        index.update_documents([updated_document], "id")

    @staticmethod
    def delete_document(document_id: int):
        index.delete_document(document_id)

    @staticmethod
    def search(query: str, params: Optional[dict[str, Any]] = None) -> list[Document]:
        default_params = {
            "attributesToCrop": ["content"],
            "attributesToHighlight": ["content"],
            "highlightPreTag": "<span class=\"highlight-text\">",
            "highlightPostTag": "</span>",
            "cropLength": 10,
        }
        if params is not None:
            default_params.update(**params)

        result = index.search(query, default_params)

        print(result)

        hits_map = map(
            lambda hit_doc: hit_doc.get("_formatted") or hit_doc, result["hits"]
        )
        return list(hits_map)

    @staticmethod
    def search_in_documents(document_ids: list[int], query: str):
        docs_str = ",".join(map(lambda i: str(i), document_ids))
        return MeiliSearchRepository.search(query, {"filter": [f"id IN [{docs_str}]"]})
