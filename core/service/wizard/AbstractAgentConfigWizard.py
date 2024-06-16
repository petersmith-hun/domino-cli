from abc import ABC, abstractmethod

from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.CommonAgentConfigWizardDataMapping import CommonMapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_AVAILABLE_LOGGING_LEVELS = ["debug", "info", "warn", "error"]
_AVAILABLE_AGENT_TYPES = ["docker", "filesystem"]
_AVAILABLE_RESULT_RENDERERS = ["console", "file"]


class AbstractAgentConfigWizard(AbstractWizard, ABC):
    """
    AbstractWizard implementation setting up the common segments of the agent configuration wizards.
    """
    def __init__(self, wizard_name: str, wizard_description: str,
                 wizard_result_transformer: AbstractWizardResultTransformer,
                 wizard_result_console_renderer: WizardResultConsoleRenderer,
                 wizard_result_file_renderer: WizardResultFileRenderer):
        super().__init__(wizard_name, wizard_description)
        self._wizard_result_transformer: AbstractWizardResultTransformer = wizard_result_transformer
        self._wizard_result_console_renderer: WizardResultConsoleRenderer = wizard_result_console_renderer
        self._wizard_result_file_renderer: WizardResultFileRenderer = wizard_result_file_renderer

    def _init_wizard(self) -> None:

        # steps
        ws_coordinator_host = BaseWizardStep(CommonMapping.COORDINATOR_HOST, "Specify Coordinator host", "ws://127.0.0.1:9987/agent")
        ws_coordinator_api_key = BaseWizardStep(CommonMapping.COORDINATOR_API_KEY, "Specify Coordinator API key")
        ws_coordinator_ping = BaseWizardStep(CommonMapping.COORDINATOR_PING, "Specify keep-alive ping interval (in Node.js 'ms' library format)")
        ws_coordinator_pong = BaseWizardStep(CommonMapping.COORDINATOR_PONG, "Specify keep-alive pong (ping response) timeout (in Node.js 'ms' library format)")

        ws_identification_host_id = BaseWizardStep(CommonMapping.IDENTIFICATION_HOST_ID, "Specify agent host ID")
        ws_identification_type = OptionSelectorWizardStep(CommonMapping.IDENTIFICATION_TYPE, "Select agent type", _AVAILABLE_AGENT_TYPES)
        ws_identification_key = BaseWizardStep(CommonMapping.IDENTIFICATION_AGENT_KEY, "Specify agent key")

        ws_logging_min_level = OptionSelectorWizardStep(CommonMapping.LOGGING_MIN_LEVEL, "Select minimum logging level", _AVAILABLE_LOGGING_LEVELS)
        ws_logging_enable_json = OptionSelectorWizardStep(CommonMapping.LOGGING_JSON, "Enable JSON logging?")

        ws_result_rendering = OptionSelectorWizardStep(CommonMapping.RESULT_RENDERING, "Write result to", _AVAILABLE_RESULT_RENDERERS)

        # transitions
        ws_coordinator_host.add_transition(ws_coordinator_api_key)
        ws_coordinator_api_key.add_transition(ws_coordinator_ping)
        ws_coordinator_ping.add_transition(ws_coordinator_pong)
        ws_coordinator_pong.add_transition(ws_identification_host_id)

        ws_identification_host_id.add_transition(ws_identification_type)
        ws_identification_type.add_transition(ws_identification_key)
        ws_identification_key.add_transition(ws_logging_min_level)

        ws_logging_min_level.add_transition(ws_logging_enable_json)

        self._chain_additional_steps(ws_logging_enable_json, ws_result_rendering)
        self.set_entry_point(ws_coordinator_host)

    @abstractmethod
    def _chain_additional_steps(self, ws_logging_enable_json: BaseWizardStep, ws_result_rendering: BaseWizardStep) -> None:
        """
        Chains further steps into the wizard flow. Actual wizard implementations must adhere to the following behavior:
         - First additional step must be chained to the ws_logging_enable_json step;
         - Last additional step must chain to the ws_result_rendering step.

        :param ws_logging_enable_json: last step of the base chain
        :param ws_result_rendering: last step of the entire wizard
        """
        pass

    def _handle_result(self, result: dict) -> None:

        transformed_result: dict = self._wizard_result_transformer.transform(result)
        if result[CommonMapping.RESULT_RENDERING.get_wizard_field()] == _AVAILABLE_RESULT_RENDERERS[0]:
            self._wizard_result_console_renderer.render(transformed_result)
        else:
            self._wizard_result_file_renderer.render(transformed_result, lambda res: res["domino"])
