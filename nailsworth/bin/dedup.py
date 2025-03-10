# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import os, re


with open("tmp/md5.txt") as f:
    hashes = [ln.strip() for ln in f.read().splitlines()]

by_hash = {}
for ln in hashes:
    [hash, file] = re.split(r"\s+", ln, maxsplit=1)
    by_hash.setdefault(hash, []).append(file)

for hash, files in by_hash.items():
    pri = sorted(files, key=lambda f: len(f))[1:]
    for file in pri:
        print(f"rm {file}")
        os.remove(file)
