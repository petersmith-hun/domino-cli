from __future__ import annotations

import yaml

from core.service.wizard.mapping.RegConfigWizardDataMapping import RegConfigWizardDataMapping as Mapping
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer


class RegConfigWizardResultTransformer(AbstractWizardResultTransformer):

    def transform(self, source: dict) -> str:

        root_node: str = source["reg_name"]
        target_dict: dict = self._define_base_dict(root_node, source)
        if self._read_current_value(Mapping.SOURCE_TYPE, root_node, target_dict) == "filesystem":
            self._add_executable_based_registration_parameters(root_node, source, target_dict)
            self._add_runtime_based_registration_parameters(root_node, source, target_dict)
            self._add_service_based_registration_parameters(root_node, source, target_dict)
        self._add_health_check_parameters(root_node, source, target_dict)

        return yaml.dump(target_dict)

    def _define_base_dict(self, root_node: str, source: dict) -> dict:

        # TODO keep order somehow
        target_dict: dict = {root_node: {}}
        self._assign(Mapping.SOURCE_TYPE, root_node, source, target_dict)
        self._assign(Mapping.EXEC_TYPE, root_node, source, target_dict)
        self._assign(Mapping.HEALTH_CHECK_ENABLE, root_node, source, target_dict, lambda value: value == "yes")

        return target_dict

    def _add_executable_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        if self._read_current_value(Mapping.EXEC_TYPE, root_node, target_dict) == "executable":
            self._add_fs_based_registration_common_parameters(root_node, source, target_dict)
            self._assign(Mapping.EXEC_USER, root_node, source, target_dict)
            self._assign(Mapping.EXEC_ARGS, root_node, source, target_dict)

    def _add_runtime_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        if self._read_current_value(Mapping.EXEC_TYPE, root_node, target_dict) == "runtime":
            self._add_fs_based_registration_common_parameters(root_node, source, target_dict)
            self._assign(Mapping.EXEC_USER, root_node, source, target_dict)
            self._assign(Mapping.EXEC_ARGS, root_node, source, target_dict)
            self._assign(Mapping.RUNTIME_NAME, root_node, source, target_dict)

    def _add_service_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        if self._read_current_value(Mapping.EXEC_TYPE, root_node, target_dict) == "service":
            self._add_fs_based_registration_common_parameters(root_node, source, target_dict)
            self._assign(Mapping.EXEC_COMMAND_NAME, root_node, source, target_dict)

    def _add_fs_based_registration_common_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        self._assign(Mapping.SOURCE_HOME, root_node, source, target_dict)
        self._assign(Mapping.BINARY_NAME, root_node, source, target_dict)

    def _add_health_check_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        if self._read_current_value(Mapping.HEALTH_CHECK_ENABLE, root_node, target_dict):
            self._assign(Mapping.HEALTH_CHECK_DELAY, root_node, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_TIMEOUT, root_node, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_MAX_ATTEMPTS, root_node, source, target_dict)
            self._assign(Mapping.HEALTH_CHECK_ENDPOINT, root_node, source, target_dict)
