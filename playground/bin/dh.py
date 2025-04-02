from collections import UserDict, UserList


def immut(*args, **kwargs):
    raise TypeError("Immutable object")


class Immutable:
    __setitem__ = immut
    __delitem__ = immut
    clear = immut
    append = immut
    extend = immut
    insert = immut
    remove = immut
    pop = immut


class ImmutableDict(Immutable, UserDict):
    pass


class ImmutableList(Immutable, UserList):
    pass


foo = ImmutableList(["a", "b", "c"])
print(foo)
# foo["a"] = 1
foo.append("d")
print(foo)
