from typing import Any


class BodyBuilder:
    def __init__(self):
        self._body = {}
        self._query = {"match_all": {}}

    def build(self) -> dict[str, Any]:
        self._body.update(query=self._query)
        return self._body

    def add_match(self, field, value):
        self._query = {}
        self._query.update(match={field: value})
        return self
