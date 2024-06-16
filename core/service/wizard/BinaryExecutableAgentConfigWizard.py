from core.service.wizard.AbstractAgentConfigWizard import AbstractAgentConfigWizard
from core.service.wizard.mapping.BinaryExecutableAgentConfigWizardDataMapping import Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.MultiAnswerWizardStep import MultiAnswerWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_WIZARD_NAME = "bin-exec-agent"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino Platform Binary Executable Agent configuration"
_AVAILABLE_SERVICE_HANDLERS = ["systemd"]


class BinaryExecutableAgentConfigWizard(AbstractAgentConfigWizard):
    """
    AbstractWizard implementation for creating Domino Platform Binary Executable Agent configurations.
    """
    def __init__(self, wizard_result_transformer: AbstractWizardResultTransformer,
                 wizard_result_console_renderer: WizardResultConsoleRenderer,
                 wizard_result_file_renderer: WizardResultFileRenderer):
        super().__init__(_WIZARD_NAME, _WIZARD_DESCRIPTION,
                         wizard_result_transformer,
                         wizard_result_console_renderer,
                         wizard_result_file_renderer)

    def _chain_additional_steps(self, ws_logging_enable_json: BaseWizardStep,
                                ws_result_rendering: BaseWizardStep) -> None:

        # steps
        ws_spawn_control_service_handler = OptionSelectorWizardStep(Mapping.SPAWN_CONTROL_SERVICE_HANDLER, "Select service handler sub-system", _AVAILABLE_SERVICE_HANDLERS)
        ws_spawn_control_start_delay = BaseWizardStep(Mapping.SPAWN_CONTROL_START_DELAY, "Specify start delay after restart (in Node.js 'ms' library format)")
        ws_spawn_control_allowed_exec_users = MultiAnswerWizardStep(Mapping.SPAWN_CONTROL_EXEC_USERS, "Specify allowed executor users")

        ws_storage_deployments = BaseWizardStep(Mapping.STORAGE_DEPLOYMENTS, "Specify storage path for deployments", "./storage/deployments")
        ws_storage_app_home = BaseWizardStep(Mapping.STORAGE_APP_HOME, "Specify home path for running apps", "./storage/home")

        ws_runtime_configure_first = OptionSelectorWizardStep(Mapping.RUNTIME_CONFIGURE_FIRST, "Do you want to configure your first runtime now?")
        ws_runtime_id = BaseWizardStep(Mapping.RUNTIME_ID, "Specify runtime ID")
        ws_runtime_binary_path = BaseWizardStep(Mapping.RUNTIME_BINARY_PATH, "Specify runtime binary path")
        ws_runtime_healthcheck = BaseWizardStep(Mapping.RUNTIME_HEALTHCHECK, "Specify runtime healthcheck command")
        ws_runtime_command_line = BaseWizardStep(Mapping.RUNTIME_COMMAND_LINE, "Specify runtime command line template")

        first_runtime_field = Mapping.RUNTIME_CONFIGURE_FIRST.get_wizard_field()

        # transitions
        ws_logging_enable_json.add_transition(ws_spawn_control_service_handler)
        ws_spawn_control_service_handler.add_transition(ws_spawn_control_start_delay)
        ws_spawn_control_start_delay.add_transition(ws_spawn_control_allowed_exec_users)
        ws_spawn_control_allowed_exec_users.add_transition(ws_storage_deployments)

        ws_storage_deployments.add_transition(ws_storage_app_home)
        ws_storage_app_home.add_transition(ws_runtime_configure_first)

        ws_runtime_configure_first.add_transition(ws_result_rendering, lambda context: context[first_runtime_field] == "no")
        ws_runtime_configure_first.add_transition(ws_runtime_id, lambda context: context[first_runtime_field] == "yes")
        ws_runtime_id.add_transition(ws_runtime_binary_path)
        ws_runtime_binary_path.add_transition(ws_runtime_healthcheck)
        ws_runtime_healthcheck.add_transition(ws_runtime_command_line)
        ws_runtime_command_line.add_transition(ws_result_rendering)
