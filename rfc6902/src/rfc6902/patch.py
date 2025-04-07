from typing import Any

from via_jsonpath import Deleted, Editor, ViaContext

from rfc6902.pointer import JsonPointer
from rfc6902.types import Patch


def rfc6902_patch(patch: Patch, obj: Any) -> Any:
    ctx = ViaContext(path="$", data=obj, up=None)
    editor = Editor()

    for op in patch:
        op_type = op["op"]
        path = JsonPointer(op["path"])

        if op_type in ("move", "copy"):
            from_path = JsonPointer(op["from"])
            value = ctx.get(from_path)
            if value is Deleted:
                raise ValueError(f"Cannot move/copy from {from_path}: not found")
            if op_type == "move":
                editor.set(from_path, Deleted)
        elif op_type == "remove":
            value = Deleted
        else:
            value = op["value"]

        if op_type == "test":
            if ctx.get(path) != value:
                raise ValueError(f"Test failed at {path}: expected {value}")
        else:
            editor.set(path, value)

    return editor.edit(obj)
