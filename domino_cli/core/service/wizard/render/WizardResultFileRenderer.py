from __future__ import annotations

from os import path
from typing import Callable

import yaml


class WizardResultFileRenderer:
    """
    File based wizard result rendering.
    """
    def render(self, result: dict, merge_node_selector_function: Callable[[dict], dict] = None) -> None:
        """
        Renders a wizard's transformed (target) dictionary object as YAML structure and writes it in the given file.
        Target file is asked by this method.
        Also using a merge function it is able to merge the results with the contents of a currently existing file.

        :param result: target dictionary to be rendered
        :param merge_node_selector_function: lambda function to select base node from where the merging should happen
        """
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
