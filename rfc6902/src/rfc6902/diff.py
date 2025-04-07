from typing import Any, Iterable

from rfc6902.pointer import JsonPointer
from rfc6902.types import Op, Patch


def enc(path: tuple) -> str:
    return str(JsonPointer(path))


def rfc6902_differ(a: Any, b: Any, path: tuple = ()) -> Iterable[Op]:
    if a is b:
        return

    elif type(a) is not type(b):
        yield {"op": "replace", "path": path, "value": b}

    elif isinstance(a, dict):
        a_keys, b_keys = set(a.keys()), set(b.keys())
        for key in a_keys - b_keys:
            yield {"op": "remove", "path": enc(path + (key,))}
        for key in b_keys - a_keys:
            yield {"op": "add", "path": enc(path + (key,)), "value": b[key]}
        for key in a_keys & b_keys:
            yield from rfc6902_diff(a[key], b[key], path + (key,))

    elif isinstance(a, list):
        a_len, b_len = len(a), len(b)
        for i in range(a_len, b_len):
            yield {"op": "add", "path": enc(path + (i,)), "value": b[i]}
        for i in range(b_len, a_len):
            yield {"op": "remove", "path": enc(path + (i,))}
        for i in range(min(a_len, b_len)):
            yield from rfc6902_diff(a[i], b[i], path + (i,))

    elif a != b:
        yield {"op": "replace", "path": enc(path), "value": b}


def rfc6902_diff(a: Any, b: Any, path: tuple = ()) -> Patch:
    return list(rfc6902_differ(a, b, path))
