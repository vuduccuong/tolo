from typing import Any

from elasticsearch.helpers import bulk

from tolo_account.serializers.user_profile import UserSerializer
from tolo_core.decorators.thread import thread_wrap
from tolo_core.helpers.utils import Utils
from tolo_core.search.base import BaseElasticSearch, SearchResult
from tolo_core.search.engine import tolo_es_enginee
from tolo_post.models import Post

_INDEX_NAME = "es_index_post"


class PostElasticSearch(BaseElasticSearch):
    def get_index_name(self):
        return _INDEX_NAME

    def create_index(self, body: dict) -> None:
        tolo_es_enginee.client.indices.create(
            index=self.get_index_name(),
            body=body,
        )

    def re_index_document(self, document_id: Any, body: dict) -> None:
        tolo_es_enginee.client.indices.create(
            index=self.get_index_name(),
            id=document_id,
            body=body,
        )

    def search(self, body: dict, **kwargs) -> SearchResult:
        return tolo_es_enginee.search(index=self.get_index_name(), body=body, **kwargs)

    @staticmethod
    def pre_index_data(post: Post) -> dict[str:Any] | None:
        author = post.author
        author_serializer = UserSerializer(author).data
        userprofile = author_serializer.get("userprofile")
        return dict(
            id=post.id,
            title=post.title,
            slug=post.slug,
            publish_date=post.publish_date,
            created_date=post.created_date,
            author=dict(
                username=author_serializer.get("username"),
                email=author_serializer.get("email"),
                userprofile=dict(userprofile),
            ),
        )

    @thread_wrap
    def bulk_save(self, index_data):
        self.init_schema()
        for data_chunks in Utils.chunks(index_data, 200):
            _, err = bulk(
                tolo_es_enginee.client,
                [
                    dict(
                        _index=self.get_index_name(),
                        _id=data.get("id"),
                        _source=data,
                    )
                    for data in data_chunks
                ],
                max_chunk_bytes=10 * 1024 * 1024,
                raise_on_error=True,
                raise_on_exception=True,
            )

            if err:
                print(err)

    def init_schema(self):
        client = tolo_es_enginee.client.indices
        existed = client.exists(index=self.get_index_name())
        if not existed:
            self.create_mapping()

    def create_mapping(self) -> None:
        schema = {
            "settings": {
                "index": {
                    "mapping": {"nested_objects": {"limit": 20000}},
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "analysis": {
                        "analyzer": {
                            "text_analyzer": {
                                "tokenizer": "text_tokenizer",
                                "filter": ["lowercase", "unique"],
                            },
                            "phone_analyzer": {
                                "tokenizer": "phone_tokenizer",
                                "filter": ["unique"],
                            },
                            "digit_analyzer": {
                                "tokenizer": "keyword",
                                "filter": ["digit_filter"],
                            },
                            "email_search_analyzer": {
                                "tokenizer": "uax_url_email",
                                "filter": [
                                    "email_search_filter",
                                    "lowercase",
                                    "unique",
                                ],
                            },
                        },
                        "tokenizer": {
                            "text_tokenizer": {
                                "type": "edge_ngram",
                                "min_gram": 2,
                                "max_gram": 32,
                                "token_chars": ["letter", "digit"],
                            },
                            "phone_tokenizer": {
                                "type": "ngram",
                                "min_gram": 2,
                                "max_gram": 12,
                                "token_chars": ["digit"],
                            },
                        },
                        "filter": {
                            "digit_filter": {
                                "type": "pattern_replace",
                                "pattern": "[^\\d]",
                                "replacement": "",
                            },
                            "email_search_filter": {
                                "type": "pattern_capture",
                                "preserve_original": True,
                                "patterns": [
                                    "([^@]+)",
                                    "(\\d{3,})",
                                    "([a-zA-Z]{3,})",
                                    "@(.+)",
                                ],
                            },
                        },
                    },
                },
                "max_ngram_diff": "50",
            },
            "mappings": {
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "search_analyzer": "standard",
                    },
                    "slug": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "search_analyzer": "standard",
                    },
                    "publish_date": {
                        "type": "date",
                        "ignore_malformed": True,
                    },
                    "created_date": {
                        "type": "date",
                        "ignore_malformed": True,
                    },
                    "author": {
                        "type": "nested",
                        "include_in_parent": True,
                        "properties": {
                            "username": {
                                "type": "text",
                                "analyzer": "text_analyzer",
                                "search_analyzer": "standard",
                            },
                            "email": {
                                "type": "text",
                                "analyzer": "text_analyzer",
                                "search_analyzer": "email_search_analyzer",
                                "index_options": "offsets",
                            },
                            "userprofile": {
                                "type": "nested",
                                "include_in_parent": True,
                                "properties": {
                                    "id": {
                                        "type": "integer",
                                    },
                                    "first_name": {
                                        "type": "text",
                                        "analyzer": "text_analyzer",
                                        "search_analyzer": "standard",
                                    },
                                    "middle_name": {
                                        "type": "text",
                                        "analyzer": "text_analyzer",
                                        "search_analyzer": "standard",
                                    },
                                    "last_name": {
                                        "type": "text",
                                        "analyzer": "text_analyzer",
                                        "search_analyzer": "standard",
                                    },
                                    "avatar": {
                                        "type": "text",
                                    },
                                    "birthday": {
                                        "type": "date",
                                        "ignore_malformed": True,
                                    },
                                    "bio": {
                                        "type": "text",
                                    },
                                },
                            },
                        },
                    },
                }
            },
        }

        self.create_index(body=schema)
