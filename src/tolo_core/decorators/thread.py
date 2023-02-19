def thread_wrap(target):
    def wrap(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        finally:
            from django.db import connections

            connections.close_all()

    return wrap
