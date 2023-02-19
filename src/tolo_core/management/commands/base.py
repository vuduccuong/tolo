from django.core.management import BaseCommand
from django.db.models import QuerySet

from tolo_core.models.query_set import ModelUtils


class BaseCommandTolo(BaseCommand):
    def handle(self, *args, **options):
        raise NotImplementedError

    @classmethod
    def queryset_iterator(cls, queryset: QuerySet, chunksize: int = 1_000):
        return ModelUtils.queryset_iterator(queryset, chunksize)
