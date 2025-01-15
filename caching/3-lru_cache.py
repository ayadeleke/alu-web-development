#!/usr/bin/python3
"""class LRUCache that inherits from BaseCaching."""


from typing import Union
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Fifo class
    Args:
        BaseCaching (class): base cache class
    """

    def __init__(self):
        super().__init__()
        self.queue = []

    def put(self, key: str, item: str) -> None:
        """Add value en cache."""
        if key and item:
            self.isFillCache(key)
            self.cache_data[key] = item

    def get(self, key: str) -> Union[None, object]:
        """Get value of cache"""
        if key not in self.cache_data.keys():
            return None
        if self.cache_data.get(key):
            self.queue.remove(key)
            self.queue.append(key)
        return self.cache_data[key]

    def isFillCache(self, key) -> None:
        """check if cache not is fill"""
        if self.cache_data.get(key):
            self.queue.remove(key)
        self.queue.append(key)
        if len(self.queue) > self.MAX_ITEMS:
            item_deleted = self.queue.pop(0)
            self.cache_data.pop(item_deleted)
            print(f'DISCARD: {item_deleted}')
