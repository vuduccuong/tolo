from contextlib import suppress


class Utils:
    @staticmethod
    def safe_int(value, default_value=0):
        with suppress(Exception):
            return int(value)
        return default_value

    @staticmethod
    def safe_bool(value, default_value=False):
        with suppress(Exception):
            return bool(value)

        return default_value

    @staticmethod
    def safe_qdict_to_dict(data, default_value):
        with suppress(Exception):
            return data.dict()

        return default_value or dict()
