from django.db.models import QuerySet


class ModelUtils:
    @classmethod
    def queryset_iterator(cls, queryset: QuerySet, chunksize: int = 1_000):
        total = queryset.count()
        for start in range(0, total, chunksize):
            end = min(start + chunksize, total)
            yield queryset[start:end], start, total
