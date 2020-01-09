from core.service.wizard.WizardStep import AbstractWizardStep


class MultiAnswerWizardStepDecorator(AbstractWizardStep):

    def __init__(self, step_id: str, question: str):
        super().__init__(step_id, question)