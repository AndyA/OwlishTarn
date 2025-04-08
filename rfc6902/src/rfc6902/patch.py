from copy import deepcopy
from functools import reduce
from typing import Any

from via_jsonpath import JPWild

from rfc6902.pointer import JsonPointer
from rfc6902.types import Patch

Ref = tuple[dict, str] | tuple[list, int]

sentinel = object()


def peek(ref: Ref) -> Any:
    obj, key = ref

    if key == JPWild:
        raise ValueError("Cannot peek virtual element")

    if isinstance(obj, dict):
        if (value := obj.get(key, sentinel)) is sentinel:
            raise ValueError(f"Key {key} not found in dict")
        return value
    elif isinstance(obj, list):
        if 0 <= key < len(obj):
            return obj[key]
        raise ValueError(f"Index {key} out of range for list")
    else:
        raise ValueError(f"Cannot get {key} from {type(obj).__name__}")


def walk(ref: Ref, path: JsonPointer) -> Ref:
    return reduce(lambda acc, key: (peek(acc), key), path, ref)


def dict_key(key: Any) -> str:
    if isinstance(key, str):
        return key

    if isinstance(key, int):
        return str(key)

    if key == JPWild:
        return "-"

    raise ValueError(f"Unsupported key type: {type(key).__name__}")


def add(ref: Ref, value: Any) -> None:
    obj, key = ref

    if isinstance(obj, dict):
        obj[dict_key(key)] = value
    elif isinstance(obj, list):
        if key == JPWild or key == len(obj):
            obj.append(value)
        elif not isinstance(key, int):
            raise ValueError(f"Key {key} must be an int for list")
        elif 0 <= key < len(obj):
            obj.insert(key, value)
        else:
            raise ValueError(f"Index {key} out of range for list")
    else:
        raise ValueError(f"Cannot add {key} to {type(obj).__name__}")


def remove(ref: Ref) -> None:
    obj, key = ref

    if isinstance(obj, dict):
        obj.pop(dict_key(key))
    elif isinstance(obj, list):
        if key == JPWild:
            raise ValueError("Cannot remove virtual element")
        elif not isinstance(key, int):
            raise ValueError(f"Key {key} must be an int for list")
        elif 0 <= key < len(obj):
            obj.pop(key)
        else:
            raise ValueError(f"Index {key} out of range for list")
    else:
        raise ValueError(f"Cannot remove {key} from {type(obj).__name__}")


def replace(ref: Ref, value: Any) -> None:
    obj, key = ref

    if key == JPWild:
        raise ValueError("Cannot replace virtual element")

    if isinstance(obj, dict):
        obj[str(key)] = value
    elif isinstance(obj, list):
        if not isinstance(key, int):
            raise ValueError(f"Key {key} must be an int for list")
        elif 0 <= key < len(obj):
            obj[key] = value
        else:
            raise ValueError(f"Index {key} out of range for list")


def rfc6902_patch(patch: Patch, obj: Any) -> Any:
    root: Ref = ({"$": deepcopy(obj)}, "$")

    def resolve(path: str) -> Ref:
        return walk(root, JsonPointer(path))

    for op in patch:
        ref = resolve(op["path"])
        match op["op"]:
            case "add":
                add(ref, deepcopy(op["value"]))
            case "remove":
                remove(ref)
            case "replace":
                replace(ref, deepcopy(op["value"]))
            case "move":
                from_ref = resolve(op["from"])
                value = peek(from_ref)
                remove(from_ref)
                add(ref, value)
            case "copy":
                add(ref, deepcopy(peek(resolve(op["from"]))))
            case "test":
                if peek(ref) != op["value"]:
                    raise ValueError(
                        f"Test failed at {op['path']}: expected {op['value']}, got: {peek(ref)}"
                    )
            case _:
                raise ValueError(f"Unknown operation: {op['op']}")

    return peek(root)
