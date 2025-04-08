from rfc6902.diff import rfc6902_diff
from rfc6902.patch import rfc6902_patch

tests = [
    {"a": 1, "b": 2},
    {"a": {"one": 1, "four": 4}, "b": {"one": 2, "three": 1}},
    {"a": [1, 2, 3], "b": [1, 2, 3, 4]},
]

for case in tests:
    print()
    a = case["a"]
    b = case["b"]
    patch = rfc6902_diff(a, b)
    c = rfc6902_patch(patch, a)
    print(f"    a: {a}")
    print(f"    b: {b}")
    print(f"patch: {patch}")
    print(f"    c: {c}")
