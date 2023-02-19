import os
from contextlib import suppress
from threading import Lock
from typing import Any
from elasticsearch import Elasticsearch

from tolo_core.helpers.utils import Utils
from tolo_core.logging.app_log import AppLog
from tolo_core.search.base import SearchResult


class SingletonMeta(type):
    __instances = dict()
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
            return cls.__instances[cls]


class ESSingleton(metaclass=SingletonMeta):
    client = None

    def __init__(self, client: Elasticsearch):
        self.client = client

    def search(self, *args, **kwargs) -> SearchResult:
        page = Utils.safe_int(kwargs.pop("page", 0))
        item_per_page = Utils.safe_int(kwargs.pop("page_size", 5000))
        from_ = page * item_per_page
        if not kwargs.get("body", {}).get("sort"):
            kwargs.get("body", {}).update(sort=[{"id": {"order": "asc"}}])
        kwargs.update(from_=from_, size=item_per_page)
        try:
            es_data = self.client.search(**kwargs, timeout="30s")
            return self._get_response(es_data, page, item_per_page)
        except Exception as e:
            AppLog.log_err(e)
        return SearchResult()

    @staticmethod
    def _get_response(
        data: dict[str, Any],
        page: int,
        item_per_page: int,
    ) -> SearchResult:
        with suppress(Exception):
            hits = data["hits"]
            total_obj = hits["total"]
            total_record = total_obj["value"]
            records = hits["hits"]
            items = list(h["_source"] for h in records)

            return SearchResult(
                page_size=item_per_page,
                page=page,
                total=total_record,
                items=items,
            )


_HOST = "localhost"
if os.environ.get("PROD"):
    _HOST = "elasticsearch"

tolo_es_enginee = ESSingleton(
    Elasticsearch(
        [
            {
                "host": _HOST,
                "port": 9200,
                "scheme": "http",
            },
        ],
    )
)
