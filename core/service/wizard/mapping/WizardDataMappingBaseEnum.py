from enum import Enum

_WIZARD_FIELD_INDEX = 0
_REGISTRATION_FIELD_INDEX = 1
_ROOT_NODE_PLACEHOLDER = "$root"


class WizardDataMappingBaseEnum(Enum):
    """
    Enum extension for holding field mapping information between raw wizard response data and target dictionaries.
    """
    def get_wizard_field(self) -> str:
        """
        Returns the raw response data field name.

        :return: the raw response data field name
        """
        return self.value[_WIZARD_FIELD_INDEX]

    def get_registration_field_reference(self, root_node: str) -> str:
        """
        Returns the target field name.
        Also able to resolve root node placeholder ('$root').

        :param root_node: name of root node in target dictionary
        :return: resolved target field name
        """
        return str(self.value[_REGISTRATION_FIELD_INDEX]).replace(_ROOT_NODE_PLACEHOLDER, root_node)
