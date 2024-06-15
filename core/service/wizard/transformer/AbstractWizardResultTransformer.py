from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, Callable

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class AbstractWizardResultTransformer(object, metaclass=ABCMeta):
    """
    Base wizard result transformer implementation providing common utility methods
    for reading source dict (raw response dictionary of wizard) and writing target
    dict ("formatted", mapped responses).
    """

    @abstractmethod
    def transform(self, source: dict) -> dict:
        """
        Transforms the given source dict to a target dict based on the implemented ruleset.

        :param source: source dict object
        :return: transformed target dict
        """
        pass

    def _assign(self, mapping: WizardDataMappingBaseEnum, root_node: str, source: dict, target_dict: dict) -> None:
        """
        Transforms a single value by doing the following steps:
         - Reads up the raw value from the source dict object using the specified field mapping.
         - Transforms the value with the given mapper function (defaults to identical mapping).
         - Writes the transformed value into the target dict object.

        :param mapping: WizardDataMappingBaseEnum object holding the field mapping information
        :param root_node: target dict object root node name (search starts from this node)
        :param source: source dict object
        :param target_dict: target dict object
        """
        key, node = self._node_search(mapping, root_node, target_dict)
        node[key] = self._safe_read(source, mapping.get_wizard_field(), mapping.get_mapper())

    def _read_current_value(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict) -> any:
        """
        Reads a single value from target dict object.

        :param mapping: WizardDataMappingBaseEnum object holding the field mapping information
        :param root_node: target dict object root node name (search starts from this node)
        :param target_dict: target dict object
        :return: retrieved value (can be any type, depends on the mapper function that created the value before)
        """
        key, node = self._node_search(mapping, root_node, target_dict)

        return node[key]

    def _node_search(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict) -> tuple:
        """
        Searches for the specified node in the target dict object for further processing.
        The returned values (as tuple) will be the following:
         - The extracted leaf key name of the given mapping.
         - The key's parent node (dict object).
        The method is also able to create the missing nodes while searching for the given node.

        :param mapping: WizardDataMappingBaseEnum object holding the field mapping information
        :param root_node: target dict object root node name (search starts from this node)
        :param target_dict: target dict object
        :return: extracted leaf key, and it's parent node as tuple
        """
        keys = mapping.get_registration_field_reference(root_node).split(".")
        max_depth: int = len(keys) - 1

        return self._recursive_search(target_dict, keys, max_depth)

    def _recursive_search(self, current_dict: dict, keys: List[str], max_depth: int, current_depth: int = 0) -> tuple:
        """
        Recursive helper method for _node_search.
        Searches with the following steps:
         - Extracts the key for the current level.
         - If the max depth is already reached based on the specified mapping, returns with the current node and key.
           With the returned key and node, data can also be read and written on this level.
           Otherwise, searching needs to go deeper:
         - First, it checks whether the currently extracted key exists on the current level of the dictionary.
           If not, initializes am empty node (dict object) on this level.
         - Then the logic enters this node and increments the depth level, and calls itself.

        :param current_dict: current node in dict object
        :param keys: identified target dictionary keys in a mapping
        :param max_depth: max depth in target dictionary (number of consecutive keys)
        :param current_depth: currently reached level in target dictionary
        :return: extracted leaf key and it's parent node as tuple
        """
        current_key = keys[current_depth]
        if current_depth < max_depth:

            if current_key not in current_dict:
                current_dict[current_key] = {}

            return self._recursive_search(current_dict[current_key], keys, max_depth, current_depth + 1)
        else:
            return current_key, current_dict

    def _safe_read(self, source: dict, key: str, mapper: Callable[[str], any]) -> any:
        """
        Able to safely read the given key of the given (raw wizard response) dict object.
        Returns None in case the key does not exist.

        :param source: source (raw wizard response) dictionary object
        :param key: key to be read
        :param mapper: mapper function to transform the read value
        :return: any type of response or None if the key does not exist in the given dict object
        """
        return mapper(source[key]) if key in source else None
