from functools import cached_property
from typing import Any, Self

from via_jsonpath import JP, JPError, JPWild


class JsonPointerError(JPError):
    pass


def enc_ptr(ptr: Any) -> str:
    if ptr == JPWild:
        return "-"
    elif isinstance(ptr, int):
        return str(ptr)
    elif isinstance(ptr, str):
        return ptr.replace("~", "~0").replace("/", "~1")
    else:
        raise TypeError(f"Unsupported type for JSON Pointer: {type(ptr)}")


def dec_ptr(ptr: str) -> Any:
    if ptr.isdigit():
        return int(ptr)
    elif ptr == "-":
        return JPWild
    else:
        return ptr.replace("~1", "/").replace("~0", "~")


class JsonPointer(JP):
    def __new__(cls, path: str | tuple) -> Self:
        if isinstance(path, cls):
            return path
        if isinstance(path, str):
            path = (*cls._parse_path(path),)
        return tuple.__new__(cls, path)

    @classmethod
    def _parse_path(cls, path: str) -> tuple:
        if path == "":
            return ()
        if path[0] != "/":
            raise JsonPointerError("Empty path")
        return (dec_ptr(part) for part in path[1:].split("/"))

    @cached_property
    def _str(self) -> str:
        return "".join("/" + enc_ptr(part) for part in self)
