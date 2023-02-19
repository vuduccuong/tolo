from threading import Thread

from tolo_core.decorators.timer import excute_time
from tolo_core.helpers.utils import Utils
from tolo_core.management.commands.base import BaseCommandTolo
from tolo_post.models import Post
from tolo_post.search import PostElasticSearch


class Command(BaseCommandTolo):
    help = "Post Elasticsearch helper"

    def add_arguments(self, parser):
        parser.add_argument("--run", dest="run")

    def handle(self, *args, **options):
        if not options:
            print(self.print_help(self.__class__, "post_es_index"))

        if ready := options.get("run"):
            if Utils.safe_int(ready) == 1:
                self.run()

    @excute_time
    def run(self):
        searcher = PostElasticSearch()

        def async_index(index_data):
            Thread(target=searcher.bulk_save, args=(index_data,)).start()

        posts = Post.objects.select_related("author").all()
        docs = []

        for post_chunks, *_ in self.queryset_iterator(posts):
            for index, post in enumerate(post_chunks):
                doc = searcher.pre_index_data(post)
                if doc:
                    docs.append(doc)
        if docs:
            async_index(docs)
