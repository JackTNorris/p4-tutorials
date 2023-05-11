from bisect import bisect_left

#creates ascending order sorted list (no duplicates). inserts items in O(n)
class KeySortedList:
    def __init__(self, key=None,  keyfunc=lambda v: v):
        self._list = []
        self._keys = []
        self._keyfunc = keyfunc

    def insert(self, item):
        k = self._keyfunc(item)  # Get key.
        try:
            #won't add key if already exists
            self._keys.index(k)
        except:
            i = bisect_left(self._keys, k)  # Determine where to insert item.
            self._keys.insert(i, k)  # Insert key of item to keys list.
            self._list.insert(i, item)  # Insert the item itself in the corresponding place.

    def retrieve_last_n(self, n):
        return list[-n:]

    def print(self):
        print(self._list)

    #TODO
    def flush():
        print("flush the list here")

    def get_last_n(self, n):
        return self._list[-n:]
