"""
JsonConverter: JSON 转换器接口
ExprNamedTupleJsonConverter: namedtuple[Expr] 转换器类
cache_to_json: 缓存返回值的装饰器
"""

import json
import os
from collections import namedtuple

CACHE_DIR = 'cache'


class JsonConverter:

    def to_json(self, obj) -> dict: raise NotImplementedError()

    def from_json(self, s): raise NotImplementedError()


def cache_to_json(cache_path: str, converter: JsonConverter):
    cache_path = os.path.join(CACHE_DIR, cache_path)

    def decorator(func):
        def wrapper(*args):
            key_str = str(args)

            if os.path.exists(cache_path):
                with open(cache_path, 'r') as fp:
                    cache = json.load(fp)
            else:
                cache = {}

            if key_str in cache:
                # print("Result loaded from cache")
                result_data = cache[key_str]
                return converter.from_json(result_data)

            # Compute the result and cache it
            result = func(*args)
            cache[key_str] = converter.to_json(result)

            with open(cache_path, 'w') as fp:
                json.dump(cache, fp)

            return result

        return wrapper

    return decorator


class NamedTupleJsonConverter(JsonConverter):
    def __init__(self, cls: type[namedtuple], to=lambda x: x, from_=lambda x: x):
        self.cls = cls
        self.to = to
        self.from_ = from_

    def to_json(self, obj: namedtuple):
        return {key: self.to(value)
                for key, value in obj._asdict().items()}

    def from_json(self, di: dict):
        return self.cls(**{key: self.from_(value)
                           for key, value in di.items()})
