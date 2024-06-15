from core.service.wizard.mapping.CoordinatorConfigWizardDataMapping import Mapping, MappingGroups

from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_ROOT = "domino"


class CoordinatorConfigWizardResultTransformer(AbstractWizardResultTransformer):
    """
    AbstractWizardResultTransformer implementation for Domino Platform Coordinator config wizard.
    """
    def transform(self, source: dict) -> dict:
        """
        Transforms the raw response data dictionary of the Coordinator config wizard to a Domino Platform Coordinator
        config compatible dictionary. Can be directly used for transforming into configuration YAML file.

        :param source: source dict object
        :return: transformed Domino Platform Coordinator configuration
        """
        target_dict: dict = {}
        self._define_base_dict(source, target_dict)
        self._add_conditional_auth_configuration(source, target_dict)
        self._add_conditional_agent_configuration(source, target_dict)

        return target_dict

    def _define_base_dict(self, source: dict, target_dict: dict) -> None:
        [self._assign(mapping, _ROOT, source, target_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.BASE)]

    def _add_conditional_auth_configuration(self, source: dict, target_dict: dict) -> None:

        if self._read_current_value(Mapping.AUTH_MODE, _ROOT, target_dict) == "direct":
            [self._assign(mapping, _ROOT, source, target_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.JWT)]

        if self._read_current_value(Mapping.AUTH_MODE, _ROOT, target_dict) == "oauth":
            [self._assign(mapping, _ROOT, source, target_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.OAUTH)]

    def _add_conditional_agent_configuration(self, source: dict, target_dict: dict) -> None:

        configure_first_agent_field = Mapping.AGENT_CONFIGURE_FIRST.get_wizard_field()

        if source[configure_first_agent_field] == "yes":
            agent_dict = dict()
            [self._assign(mapping, _ROOT, source, agent_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.FIRST_AGENT)]

            source[configure_first_agent_field] = [agent_dict]
            self._assign(Mapping.AGENT_CONFIGURE_FIRST, _ROOT, source, target_dict)
