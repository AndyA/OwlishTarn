import glob
import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Self

import imagehash
from mistralai import Callable, Optional
from PIL import Image


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


def save_json(file: str, data: Any) -> None:
    os.makedirs(os.path.dirname(file), exist_ok=True)
    tmp = file + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps(data, indent=2))
    os.rename(tmp, file)


def load_json(file: str) -> Any:
    with open(file) as f:
        return json.load(f)


def make_hashes(dir: str) -> None:
    rows = []
    for img in glob.glob(os.path.join(dir, "**/*"), recursive=True):
        print(f"Processing {img}")
        i = Image.open(img)
        hash = int(str(imagehash.phash(i)), 16)
        rec = {
            "img": img,
            "hash": hash,
            "size": i.size,
            "file_size": os.path.getsize(img),
        }
        rows.append(rec)
    return rows


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


HASHES = "tmp/hashes.json"

try:
    hashes = load_json(HASHES)
except FileNotFoundError:
    hashes = make_hashes("images")
    save_json(HASHES, hashes)

by_hash = {}
for row in hashes:
    by_hash.setdefault(row["hash"], []).append(row)

tree = BKTree[int](distance=hamming)
for row in hashes:
    tree.insert(row["hash"])


for row in hashes:
    group = []
    for dist, hash in tree.search(row["hash"], 5):
        group += by_hash[hash]
    if len(group) > 1:
        group.sort(key=lambda x: x["file_size"], reverse=True)
        print(json.dumps(group[:]))
