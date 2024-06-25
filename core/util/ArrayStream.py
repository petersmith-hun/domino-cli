from __future__ import annotations

from typing import List, Callable


class ArrayStream:
    """
    Helper class to use expression chains on the given array.
    """
    def __init__(self, array: List[any]):
        self._array = array

    def filter(self, filter_expression: Callable[[any], bool]) -> ArrayStream:
        """
        Filters data in the wrapped array.
        :param filter_expression: filter expression to run on the wrapped array
        :return: wrapper object for expression chaining
        """
        self._array = list(filter(filter_expression, self._array))

        return self

    def sort(self, sort_by: Callable[[any], any]) -> ArrayStream:
        """
        Sorts the wrapped array by the given sort key.
        :param sort_by: sort key expression
        :return: wrapper object for expression chaining
        """
        self._array.sort(key=sort_by)

        return self

    def last(self) -> any:
        """
        Closes the wrapper and returns the last item of the wrapped array.
        :return: last item of the wrapped array
        """
        return self._array.pop()
