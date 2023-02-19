from contextlib import suppress
from dataclasses import field


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
    def safe_qdict_to_dict(data, default_value: dict = None):
        with suppress(Exception):
            return data.dict()

        return default_value or dict()

    @staticmethod
    def chunks(list_: list, s: int):
        """
        Chunk list
        Input: [1,2,3,4,5,6,7], 2
        :param list_: list
        :param s: size
        :return: [1, 2], [3, 4], [5, 6], [7]
        """
        list_ = list(list_)
        for i in range(0, len(list_), s):
            yield list_[i : i + s]
