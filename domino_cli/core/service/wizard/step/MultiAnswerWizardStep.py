from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from domino_cli.core.service.wizard.step.BaseWizardStep import BaseWizardStep


class MultiAnswerWizardStep(BaseWizardStep):
    """
    BaseWizardStep implementation to create wizard steps generating the response model as list.
    """
    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str):
        super().__init__(step_id, "{0} (one at a line, empty line to stop)".format(question))

    def read_answer(self, result: dict) -> None:
        """
        Reads answers from stdin. Multiple answers are expected from stdin until an empty line is provided.

        :param result: dictionary to be used to collect answers
        """
        result[self.get_step_id()] = []
        while True:
            current_answer: str = input()
            if len(current_answer) > 0:
                result[self.get_step_id()].append(current_answer)
            else:
                break
