from __future__ import annotations

from difflib import SequenceMatcher
from typing import List, Optional

import certifi

from nemoguardrails import LLMRails
from nemoguardrails.rails.llm.config import RailsConfig
from nemoguardrails.embeddings.index import EmbeddingsIndex, IndexItem
from nemoguardrails.rails.llm.config import EmbeddingsCacheConfig


class SimpleEmbeddingSearchProvider(EmbeddingsIndex):
    """A tiny local embedding-search provider.

    This avoids downloading embedding models (e.g. FastEmbed/HF) and is enough for
    minimal demos where we only have a handful of examples.
    """

    def __init__(self, *args, **kwargs):
        self._items: List[IndexItem] = []
        self._cache_config = EmbeddingsCacheConfig(enabled=False)

    @property
    def embedding_size(self):
        return 0

    @property
    def cache_config(self):
        return self._cache_config

    async def _get_embeddings(self, texts: List[str]):
        return None

    async def add_item(self, item: IndexItem):
        self._items.append(item)

    async def add_items(self, items: List[IndexItem]):
        self._items.extend(items)

    async def search(self, text: str, max_results: int, threshold: Optional[float]):
        if not self._items:
            return []

        # Normalize threshold to something sensible for SequenceMatcher ratios.
        thr = 0.0 if threshold is None else float(threshold)

        scored: List[tuple[float, IndexItem]] = []
        for it in self._items:
            score = SequenceMatcher(a=text.lower(), b=it.text.lower()).ratio()
            if score >= thr:
                scored.append((score, it))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [it for _, it in scored[:max_results]]



def init(app: LLMRails):
    app.register_embedding_search_provider("simple", SimpleEmbeddingSearchProvider)

