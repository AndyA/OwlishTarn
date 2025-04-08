from copy import copy
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional, Self

from rfc6902.patch import rfc6902_patch


@dataclass(frozen=True, kw_only=True)
class VersionedDoc:
    doc: Any
    patches_key: str = "patches"

    @cached_property
    def patches(self) -> list[dict[str, Any]]:
        return self.doc.get(self.patches_key, [])

    @cached_property
    def bare(self) -> Any:
        doc = copy(self.doc)
        doc.pop(self.patches_key, None)
        return doc

    @cached_property
    def previous(self) -> Optional[Self]:
        patches = copy(self.patches)
        while patches:
            last_patch = patches.pop()
            if not last_patch:  # empty?
                continue
            prev = rfc6902_patch(last_patch, self.bare)
            return type(self)(
                doc=prev | {self.patches_key: patches},
                patches_key=self.patches_key,
            )

        return None

    @cached_property
    def versions(self):
        versions = []
        ver = self
        while ver:
            versions.append(ver)
            ver = ver.previous
        return versions
