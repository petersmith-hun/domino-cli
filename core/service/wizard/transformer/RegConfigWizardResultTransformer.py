from __future__ import annotations
from collections import Callable

import yaml

from core.service.wizard.mapping.RegConfigWizardDataMapping import RegConfigWizardDataMapping as Mapping
from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer


class RegConfigWizardResultTransformer(AbstractWizardResultTransformer):

    def transform(self, source: dict) -> str:

        target_dict: dict = self._define_base_dict(source)
        if source["source_type"] == "filesystem":
            self._add_executable_based_registration_parameters(source, target_dict)
            self._add_runtime_based_registration_parameters(source, target_dict)
            self._add_service_based_registration_parameters(source, target_dict)
        self._add_health_check_parameters(source, target_dict)

        return yaml.dump(target_dict)

    def _define_base_dict(self, source: dict) -> dict:

        # TODO keep order somehow
        target_dict: dict = {source["reg_name"]: {}}
        self._assign(Mapping.SOURCE_TYPE, source, target_dict)
        self._assign(Mapping.EXEC_TYPE, source, target_dict)
        self._assign(Mapping.HEALTH_CHECK_ENABLE, source, target_dict, lambda value: value == "yes")

        return target_dict

    def _add_executable_based_registration_parameters(self, source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "executable":
            self._add_fs_based_registration_common_parameters(source, target_dict)
            self._assign(Mapping.EXEC_USER, source, target_dict)
            self._assign(Mapping.EXEC_ARGS, source, target_dict)

    def _add_runtime_based_registration_parameters(self, source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "runtime":
            self._add_fs_based_registration_common_parameters(source, target_dict)
            self._assign(Mapping.EXEC_USER, source, target_dict)
            self._assign(Mapping.EXEC_ARGS, source, target_dict)
            self._assign(Mapping.RUNTIME_NAME, source, target_dict)

    def _add_service_based_registration_parameters(self, source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "service":
            self._add_fs_based_registration_common_parameters(source, target_dict)
            self._assign(Mapping.EXEC_COMMAND_NAME, source, target_dict)

    def _add_fs_based_registration_common_parameters(self, source: dict, target_dict: dict) -> None:

        self._assign(Mapping.SOURCE_HOME, source, target_dict)
        self._assign(Mapping.BINARY_NAME, source, target_dict)

    def _add_health_check_parameters(self, source: dict, target_dict: dict) -> None:

        if target_dict[source["reg_name"]]["health-check"]["enabled"]:
            self._assign(Mapping.HEALTH_CHECK_DELAY, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_TIMEOUT, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_MAX_ATTEMPTS, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_ENDPOINT, source, target_dict)

    def _assign(self, mapping: WizardDataMappingBaseEnum, source: dict, target_dict: dict, mapper: Callable[[str], any] = lambda value: value) -> None:

        current_dict_node: dict = target_dict
        keys = mapping.get_registration_field_reference(source["reg_name"]).split(".")
        index: int = 1  # TODO lil' bit dirty solution, clean it up
        depth: int = len(keys)
        for key in keys:
            if index < depth:

                if key not in current_dict_node:
                    current_dict_node[key] = {}

                current_dict_node = current_dict_node[key]
                index = index + 1
            else:
                current_dict_node[key] = self._safe_read(source, mapping.get_wizard_field(), mapper)

    def _safe_read(self, source: dict, key: str, mapper: Callable[[str], any]):
        return mapper(source[key]) if key in source else None
