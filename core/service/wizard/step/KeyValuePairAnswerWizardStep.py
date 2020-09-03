from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from core.service.wizard.step.BaseWizardStep import BaseWizardStep


class KeyValuePairAnswerWizardStep(BaseWizardStep):
    """
    BaseWizardStep implementation to create wizard steps generating the response model as map.
    """
    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str):
        super().__init__(step_id, question)
