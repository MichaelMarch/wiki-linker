# This class relies on a feature of Python 3.7+ which guarantees that dictionaries preserve order on insertion.

# The class provides O(1) look up of elements while keeping the order and sacrificing the memory.
# All items of this collection are unique
class OrderedSet:
    def __init__(self):
        self.set: set = set()
        self.map: dict = {}

    def __len__(self) -> int:
        return len(self.map.keys())

    def __contains__(self, value) -> bool:
        return value in self.map

    def add(self, value):
        if value not in self.map:
            self.map[value] = None
            self.set.add(value)
    
    def __iter__(self):
        yield from self.map.keys()

    def count_intersections_with(self, ordered_set: "OrderedSet") -> int:
        return len(set.intersection(self.set, ordered_set.set))

    def get(self, index: int):
        return list(self.map.keys())[index]

    def slice(self, from_index: int, to_index: int):
        return list(self.map.keys())[from_index: to_index]

    def remove(self, value):
        del self.map[value]
        self.set.discard(value)
