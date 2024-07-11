from __future__ import annotations

from enum import Enum
from typing import Callable, List

from domino_cli.core.service.utility.BCryptUtil import encrypt

_MAPPING_GROUP = 0
_WIZARD_FIELD_INDEX = 1
_REGISTRATION_FIELD_INDEX = 2
_MAPPER_FIELD_INDEX = 3
_ROOT_NODE_PLACEHOLDER = "$root"

_DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER = (lambda value: value == "yes")
_UPPERCASE_MAPPER = (lambda value: str(value).upper())
_STR_TO_INT_MAPPER = (lambda value: int(value))
_BCRYPT_MAPPER = encrypt


class WizardDataMappingBaseEnum(Enum):
    """
    Enum extension for holding field mapping information between raw wizard response data and target dictionaries.
    """
    def get_mapping_group(self) -> Enum:
        """
        Returns the assigned mapping group.

        :return: assigned mapping group
        """
        return self.value[_MAPPING_GROUP]

    def get_wizard_field(self) -> str:
        """
        Returns the raw response data field name.

        :return: the raw response data field name
        """
        return self.value[_WIZARD_FIELD_INDEX]

    def get_registration_field_reference(self, root_node: str) -> str:
        """
        Returns the target field name.
        Also, able to resolve root node placeholder ('$root').

        :param root_node: name of root node in target dictionary
        :return: resolved target field name
        """
        return str(self.value[_REGISTRATION_FIELD_INDEX]).replace(_ROOT_NODE_PLACEHOLDER, root_node)

    def get_mapper(self) -> Callable[[str], any]:
        """
        Returns the assigned mapper function, or identity if not provided.

        :return: assigned mapper function
        """
        return (lambda value: value) \
            if len(self.value) < 4 \
            else self.value[_MAPPER_FIELD_INDEX]

    @classmethod
    def get_mappings_by_group(cls, group: Enum) -> List[WizardDataMappingBaseEnum]:
        """
        Returns all mapping assigned to the given mapping group.

        :param group: mapping group name as enum constant
        :return: assigned mappings
        """
        return [item for item in cls if item.get_mapping_group() == group]
