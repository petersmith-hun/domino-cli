from domino_cli.core.cli.Logging import warning
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from domino_cli.core.service.wizard.step.BaseWizardStep import BaseWizardStep


class KeyValuePairAnswerWizardStep(BaseWizardStep):
    """
    BaseWizardStep implementation to create wizard steps generating the response model as map.
    """
    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str):
        super().__init__(step_id, "{0} (in key:value format, empty line to stop)".format(question))

    def read_answer(self, result: dict) -> None:
        """
        Reads answers from stdin. Multiple answers are expected from stdin until an empty line is provided.
        The answers must be provided in 'key:value' format (key and value separated by a colon).

        :param result: dictionary to be used to collect answers
        """
        result[self.get_step_id()] = dict()
        while True:
            current_answer: str = RuntimeHelper.input_wrapper(lambda: input())
            if len(current_answer) > 0:
                split_answer = current_answer.split(sep=":", maxsplit=1)
                try:
                    result[self.get_step_id()][split_answer[0]] = split_answer[1]
                except IndexError:
                    warning("Invalid format - please specify your answer in key:value format")
                    continue
            else:
                break
