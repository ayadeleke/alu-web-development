#!/usr/bin/python3
"""class FIFOCache that inherits from BaseCaching."""


from typing import Union
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Fifo class
    Args:
        BaseCaching (class): base cache class
    """

    def __init__(self):
        super().__init__()

    def put(self, key: str, item: str) -> None:
        """Add value en cache."""
        if key and item:
            new_dict = {key: item}
            self.isFillCache()
            new_dict.update(self.cache_data)
            self.cache_data = new_dict

    def get(self, key: str) -> Union[None, object]:
        """Get value of cache"""
        if key not in self.cache_data.keys():
            return None
        return self.cache_data[key]

    def isFillCache(self) -> None:
        """check if cache not is fill"""
        if len(self.cache_data.keys()) >= self.MAX_ITEMS:
            delete_item = self.cache_data.popitem()[0]
            print(f'DISCARD: {delete_item}')
