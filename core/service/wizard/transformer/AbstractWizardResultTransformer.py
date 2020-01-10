from __future__ import annotations
from abc import ABCMeta, abstractmethod
from collections import Callable
from typing import List

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class AbstractWizardResultTransformer(object, metaclass=ABCMeta):

    @abstractmethod
    def transform(self, source: dict) -> str:
        pass

    def _assign(self, mapping: WizardDataMappingBaseEnum, root_node: str, source: dict, target_dict: dict, mapper: Callable[[str], any] = lambda value: value) -> None:

        key, node = self._node_search(mapping, root_node, target_dict)
        node[key] = self._safe_read(source, mapping.get_wizard_field(), mapper)

    def _read_current_value(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict) -> any:

        key, node = self._node_search(mapping, root_node, target_dict)

        return node[key]

    def _node_search(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict) -> tuple:

        keys = mapping.get_registration_field_reference(root_node).split(".")
        max_depth: int = len(keys) - 1

        return self._recursive_search(target_dict, keys, max_depth)

    def _recursive_search(self, current_dict: dict, keys: List[str], max_depth: int, current_depth: int = 0) -> tuple:

        current_key = keys[current_depth]
        if current_depth < max_depth:

            if current_key not in current_dict:
                current_dict[current_key] = {}

            return self._recursive_search(current_dict[current_key], keys, max_depth, current_depth + 1)
        else:
            return current_key, current_dict

    def _safe_read(self, source: dict, key: str, mapper: Callable[[str], any]) -> any:
        return mapper(source[key]) if key in source else None
