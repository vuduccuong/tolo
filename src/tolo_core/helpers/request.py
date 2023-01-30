from tolo_core.middlewares.current_request import get_current_request


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, "user", None)
