from __future__ import annotations
from collections import Callable
from os import path

import yaml


class WizardResultFileRenderer:

    def render(self, result: dict, merge_node_selector_function: Callable[[dict], dict] = None) -> None:

        target_file: str = input("File path > ")
        to_write: dict = self._prepare_dict_to_write(target_file, result, merge_node_selector_function)
        with open(target_file, "w") as target_file:
            yaml.dump(to_write, target_file, sort_keys=False)

    def _prepare_dict_to_write(self, target_file: str, result: dict, merge_node_selector_function: Callable[[dict], dict]) -> dict:

        to_write: dict = result
        if merge_node_selector_function is not None and path.exists(target_file):
            with open(target_file, "r") as current_file:
                to_write = yaml.load(current_file, Loader=yaml.SafeLoader)
                merge_node_selector_function(to_write).update(merge_node_selector_function(result))

        return to_write
