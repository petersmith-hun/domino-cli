from __future__ import annotations

import yaml

from core.service.wizard.mapping.RegConfigWizardDataMapping import RegConfigWizardDataMapping as Mapping
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer


_SOURCE_TYPE_FILESYSTEM = "FILESYSTEM"
_EXEC_TYPE_EXECUTABLE = "EXECUTABLE"
_EXEC_TYPE_RUNTIME = "RUNTIME"
_EXEC_TYPE_SERVICE = "SERVICE"

_REGISTRATION_ROOT = "domino.registrations.{0}"
_DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER = (lambda value: value == "yes")
_UPPERCASE_MAPPER = (lambda value: str(value).upper())


class RegConfigWizardResultTransformer(AbstractWizardResultTransformer):

    def __init__(self):
        self._exec_type_parameter_filler_mapping = {
            _EXEC_TYPE_EXECUTABLE: self._add_executable_based_registration_parameters,
            _EXEC_TYPE_RUNTIME: self._add_runtime_based_registration_parameters,
            _EXEC_TYPE_SERVICE: self._add_service_based_registration_parameters
        }

    def transform(self, source: dict) -> str:

        root_node: str = _REGISTRATION_ROOT.format(source[Mapping.REGISTRATION_NAME.get_wizard_field()])
        target_dict: dict = self._define_base_dict(root_node, source)
        if self._read_current_value(Mapping.SOURCE_TYPE, root_node, target_dict) == _SOURCE_TYPE_FILESYSTEM:
            exec_type: str = self._read_current_value(Mapping.EXEC_TYPE, root_node, target_dict)
            self._exec_type_parameter_filler_mapping.get(exec_type)(root_node, source, target_dict)
        self._add_health_check_parameters(root_node, source, target_dict)

        return yaml.dump(target_dict, sort_keys=False)

    def _define_base_dict(self, root_node: str, source: dict) -> dict:

        target_dict: dict = {}
        self._assign(Mapping.SOURCE_TYPE, root_node, source, target_dict, _UPPERCASE_MAPPER)
        self._assign(Mapping.EXEC_TYPE, root_node, source, target_dict, _UPPERCASE_MAPPER)
        self._assign(Mapping.HEALTH_CHECK_ENABLE, root_node, source, target_dict, _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)

        return target_dict

    def _add_executable_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        self._add_fs_based_registration_common_parameters(root_node, source, target_dict)
        self._assign(Mapping.EXEC_USER, root_node, source, target_dict)
        self._assign(Mapping.EXEC_ARGS, root_node, source, target_dict)

    def _add_runtime_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

        self._add_fs_based_registration_common_parameters(root_node, source, target_dict)
        self._assign(Mapping.EXEC_USER, root_node, source, target_dict)
        self._assign(Mapping.EXEC_ARGS, root_node, source, target_dict)
        self._assign(Mapping.RUNTIME_NAME, root_node, source, target_dict)

    def _add_service_based_registration_parameters(self, root_node: str, source: dict, target_dict: dict) -> None:

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
