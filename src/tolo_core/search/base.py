import abc
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class SearchResult:
    total: int = 0
    items: List[Any] = field(default_factory=list)
    page: int = 1
    page_size: int = 20

    def get_response(self) -> dict[str, Any]:
        return dict(
            total=self.total,
            items=self.items,
            page=self.page,
            page_size=self.page_size,
        )


class BaseElasticSearch(abc.ABC):
    @abstractmethod
    def get_index_name(self):
        ...

    @abstractmethod
    def create_index(self, body: dict) -> None:
        ...

    @abstractmethod
    def re_index_document(self, document_id: Any, body: dict) -> None:
        ...

    @abstractmethod
    def search(self, query: Any, body: dict) -> SearchResult:
        ...
