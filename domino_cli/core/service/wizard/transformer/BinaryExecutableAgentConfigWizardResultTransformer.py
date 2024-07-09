from domino_cli.core.service.wizard.mapping.BinaryExecutableAgentConfigWizardDataMapping import Mapping, MappingGroups
from domino_cli.core.service.wizard.mapping.CommonAgentConfigWizardDataMapping import CommonMapping, CommonMappingGroups
from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_ROOT = "domino"


class BinaryExecutableAgentConfigWizardResultTransformer(AbstractWizardResultTransformer):
    """
    AbstractWizardResultTransformer implementation for Domino Platform Binary Executable Agent config wizard.
    """
    def transform(self, source: dict) -> dict:
        """
        Transforms the raw response data dictionary of the Binary Executable Agent config wizard to a Domino Platform
        Binary Executable Agent config compatible dictionary. Can be directly used for transforming into configuration YAML file.

        :param source: source dict object
        :return: transformed Domino Platform Binary Executable Agent configuration
        """
        target_dict: dict = {}
        self._define_base_dict(source, target_dict)
        self._add_conditional_runtime_configuration(source, target_dict)

        return target_dict

    def _define_base_dict(self, source: dict, target_dict: dict) -> None:
        [self._assign(mapping, _ROOT, source, target_dict) for mapping in CommonMapping.get_mappings_by_group(CommonMappingGroups.BASE)]
        [self._assign(mapping, _ROOT, source, target_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.BASE)]

    def _add_conditional_runtime_configuration(self, source: dict, target_dict: dict) -> None:

        configure_first_runtime_field = Mapping.RUNTIME_CONFIGURE_FIRST.get_wizard_field()

        if source[configure_first_runtime_field] == "yes":
            agent_dict = dict()
            [self._assign(mapping, _ROOT, source, agent_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.FIRST_RUNTIME)]

            source[configure_first_runtime_field] = [agent_dict]
            self._assign(Mapping.RUNTIME_CONFIGURE_FIRST, _ROOT, source, target_dict)
