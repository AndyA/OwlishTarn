from typing import List, Literal, TypedDict, Union

AddOp = TypedDict("AddOp", {"op": Literal["add"], "path": str, "value": str})
RemOp = TypedDict("RemOp", {"op": Literal["remove"], "path": str})
ReplOp = TypedDict("ReplOp", {"op": Literal["replace"], "path": str, "value": str})
MoveOp = TypedDict("MoveOp", {"op": Literal["move"], "from": str, "path": str})
CopyOp = TypedDict("CopyOp", {"op": Literal["copy"], "from": str, "path": str})
TestOp = TypedDict("TestOp", {"op": Literal["test"], "path": str, "value": str})
Op = Union[AddOp, RemOp, ReplOp, MoveOp, CopyOp, TestOp]
Patch = List[Op]
