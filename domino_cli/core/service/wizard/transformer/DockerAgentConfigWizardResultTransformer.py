from domino_cli.core.service.wizard.mapping.CommonAgentConfigWizardDataMapping import CommonMappingGroups, CommonMapping
from domino_cli.core.service.wizard.mapping.DockerAgentConfigWizardDataMapping import Mapping, MappingGroups
from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_ROOT = "domino"


class DockerAgentConfigWizardResultTransformer(AbstractWizardResultTransformer):
    """
    AbstractWizardResultTransformer implementation for Domino Platform Docker Agent config wizard.
    """
    def transform(self, source: dict) -> dict:
        """
        Transforms the raw response data dictionary of the Docker Agent config wizard to a Domino Platform Docker Agent
        config compatible dictionary. Can be directly used for transforming into configuration YAML file.

        :param source: source dict object
        :return: transformed Domino Platform Docker Agent configuration
        """
        target_dict: dict = {}
        self._define_base_dict(source, target_dict)
        self._add_conditional_server_configuration(source, target_dict)

        return target_dict

    def _define_base_dict(self, source: dict, target_dict: dict) -> None:
        [self._assign(mapping, _ROOT, source, target_dict) for mapping in CommonMapping.get_mappings_by_group(CommonMappingGroups.BASE)]
        [self._assign(mapping, _ROOT, source, target_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.BASE)]

    def _add_conditional_server_configuration(self, source: dict, target_dict: dict) -> None:

        configure_first_server_field = Mapping.DOCKER_CONFIGURE_FIRST.get_wizard_field()

        if source[configure_first_server_field] == "yes":
            agent_dict = dict()
            [self._assign(mapping, _ROOT, source, agent_dict) for mapping in Mapping.get_mappings_by_group(MappingGroups.FIRST_SERVER)]

            source[configure_first_server_field] = [agent_dict]
            self._assign(Mapping.DOCKER_CONFIGURE_FIRST, _ROOT, source, target_dict)
