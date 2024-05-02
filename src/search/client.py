import meilisearch

from ..settings import settings

__all__ = ("client", "index")

client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILI_MASTER_KEY)
index = client.index("contents")
