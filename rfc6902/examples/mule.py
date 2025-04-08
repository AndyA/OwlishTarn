import hashlib
import json
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from functools import cached_property
from typing import Any, Callable, Iterable, Optional, Self


@dataclass(frozen=True, kw_only=True)
class BKNode[T]:
    nodes: dict[int, Self] = field(default_factory=dict)
    data: T


type DistanceFunction[T] = Callable[[T, T], int]


@dataclass(kw_only=True)
class BKTree[T]:
    distance: DistanceFunction[T]
    root: Optional[BKNode[T]] = None

    def _insert(self, node: Optional[BKNode[T]], value: T):
        if not node:
            return BKNode(data=value)

        dist = self.distance(node.data, value)

        if dist == 0:
            return node
        elif dist in node.nodes:
            self._insert(node.nodes[dist], value)
        else:
            node.nodes[dist] = BKNode(data=value)

        return node

    def _search(
        self, node: Optional[BKNode[T]], value: T, threshold: int
    ) -> Iterable[tuple[int, T]]:
        if not node:
            return

        dist = self.distance(node.data, value)

        if dist <= threshold:
            yield dist, node.data

        for d in range(max(1, dist - threshold), dist + threshold + 1):
            if d in node.nodes:
                yield from self._search(node.nodes[d], value, threshold)

    def insert(self, value: T):
        self.root = self._insert(self.root, value)

    def search(self, value: T, threshold: int) -> Iterable[tuple[int, T]]:
        yield from self._search(self.root, value, threshold)


@dataclass(frozen=True, kw_only=True)
class DataHasher:
    cache: dict[int, str] = field(default_factory=dict)

    def hash(self, data: Any) -> str:
        data_id = id(data)
        if data_id in self.cache:
            return self.cache[data_id]

        if isinstance(data, list):
            parts = tuple(self.hash(item) for item in data)
        elif isinstance(data, dict):
            parts = tuple(
                i for key in sorted(data.keys()) for i in (key, self.hash(data[key]))
            )
        else:
            parts = (json.dumps(data),)

        plain = " ".join((type(data).__name__, *parts))
        hash = hashlib.sha256(plain.encode()).hexdigest()
        self.cache[data_id] = hash

        return hash


@dataclass(frozen=True, kw_only=True)
class Leaf:
    path: tuple
    value: str


def walk_object(obj: Any, path: tuple = ()) -> Iterable[tuple[tuple, str]]:
    if isinstance(obj, (dict, list)):
        if not len(obj):
            yield Leaf(path=path, value=json.dumps(obj))
        elif isinstance(obj, dict):
            for key in sorted(obj.keys()):
                yield from walk_object(obj[key], path + (key,))
        else:
            for index, value in enumerate(obj):
                yield from walk_object(value, path + (index,))
    else:
        yield Leaf(path=path, value=json.dumps(obj))


@dataclass(frozen=True, kw_only=True)
class DataShape:
    data: Any

    @cached_property
    def shape(self) -> list[Leaf]:
        return list(walk_object(self.data))

    @cached_property
    def by_path(self) -> dict[tuple, str]:
        return {leaf.path: leaf.value for leaf in self.shape}

    @cached_property
    def paths(self) -> list[tuple]:
        return [leaf.path for leaf in self.shape]

    @cached_property
    def values(self) -> list[str]:
        return [leaf.value for leaf in self.shape]


@dataclass(frozen=True, kw_only=True)
class LeafPair:
    path: tuple
    left: str
    right: str


@dataclass(frozen=True, kw_only=True)
class ShapeDiff:
    left: DataShape
    right: DataShape

    @cached_property
    def paths(self) -> list[tuple]:
        return sorted(list(set(self.left.paths) | set(self.right.paths)))

    @cached_property
    def matcher(self):
        return SequenceMatcher(
            isjunk=None,
            a=self.left.values,
            b=self.right.values,
            autojunk=False,
        )

    @cached_property
    def foofoo(self):
        left_paths = self.left.paths
        right_paths = self.right.paths
        return [
            (op, left_paths[l1:l2], right_paths[r1:r2])
            for op, l1, l2, r1, r2 in self.matcher.get_opcodes()
        ]


left = {
    "a": {"name": "foo", "email": "foo@googoo.poo", "nick": "FooFoo"},
    "b": {"b": {"c": 1, "d": 2}, "e": 3},
    "f": [4, 5, 6, 7],
    "g": {},
    "h": {"name": "foo"},
}

right = {
    "a": {"b": {"c": 1, "d": 3, "i": False}, "e": 3},
    "f": [4, 5, 6],
    "h": {"name": "foo", "email": "foo@googoo.poo", "nick": "FooFoo"},
}

diff = ShapeDiff(left=DataShape(data=left), right=DataShape(data=right))

for op in diff.foofoo:
    print(op)
