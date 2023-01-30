from threading import local

tolo_global = local()


def get_current_request():
    return getattr(tolo_global, "request", None)


def reset_current_request():
    return setattr(tolo_global, "request", None)


class RequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(tolo_global, "request"):
            from rest_framework.request import Request
            from rest_framework.parsers import JSONParser

            tolo_global.request = Request(request, parsers=[JSONParser()])
        return self.get_response(request)
