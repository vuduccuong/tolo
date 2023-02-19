import functools
import time


def excute_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        rest = func(*args, **kwargs)
        print(f"It take time: {time.time() - start}ms")
        return rest

    return wrapper
