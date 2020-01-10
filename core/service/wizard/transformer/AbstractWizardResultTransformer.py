from __future__ import annotations
from abc import ABCMeta, abstractmethod
from collections import Callable

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class AbstractWizardResultTransformer(object, metaclass=ABCMeta):

    @abstractmethod
    def transform(self, source: dict) -> str:
        pass

    def _assign(self, mapping: WizardDataMappingBaseEnum, root_node: str, source: dict, target_dict: dict, mapper: Callable[[str], any] = lambda value: value) -> None:

        key, node = self._node_search(mapping, root_node, target_dict)
        node[key] = self._safe_read(source, mapping.get_wizard_field(), mapper)

    def _read_current_value(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict) -> None:

        key, node = self._node_search(mapping, root_node, target_dict)

        return node[key]

    def _node_search(self, mapping: WizardDataMappingBaseEnum, root_node: str, target_dict: dict):

        current_dict_node: dict = target_dict
        keys = mapping.get_registration_field_reference(root_node).split(".")
        index: int = 1  # TODO lil' bit dirty solution, clean it up
        depth: int = len(keys)
        key = None
        for key in keys:
            if index < depth:

                if key not in current_dict_node:
                    current_dict_node[key] = {}

                current_dict_node = current_dict_node[key]
                index = index + 1

        return key, current_dict_node

    def _safe_read(self, source: dict, key: str, mapper: Callable[[str], any]):
        return mapper(source[key]) if key in source else None
