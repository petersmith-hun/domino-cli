import yaml

from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer
from domino_cli.core.tui.modals.wizards import BaseWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import WizardResultModal, ConfigType


class CommonConfigWizardModal(BaseWizardModal):

    def __init__(self, config_type: ConfigType, abstract_wizard_result_transformer: AbstractWizardResultTransformer):
        super().__init__()
        self._config_type = config_type
        self._abstract_wizard_result_transformer = abstract_wizard_result_transformer

    def _handle_result(self, responses: dict[str, str | list[str]]) -> None:
        transformed = self._abstract_wizard_result_transformer.transform(responses)
        yaml_result = yaml.dump(transformed, sort_keys=False)
        self.app.push_screen(WizardResultModal(self._config_type, yaml_result))
