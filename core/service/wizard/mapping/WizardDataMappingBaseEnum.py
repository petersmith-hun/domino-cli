from enum import Enum

_WIZARD_FIELD_INDEX = 0
_REGISTRATION_FIELD_INDEX = 1
_ROOT_NODE_PLACEHOLDER = "$root"


class WizardDataMappingBaseEnum(Enum):

    def get_wizard_field(self) -> str:
        return self.value[_WIZARD_FIELD_INDEX]

    def get_registration_field_reference(self, root_node: str) -> str:
        return str(self.value[_REGISTRATION_FIELD_INDEX]).replace(_ROOT_NODE_PLACEHOLDER, root_node)
