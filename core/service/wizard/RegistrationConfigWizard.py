from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.RegConfigWizardDataMapping import RegConfigWizardDataMapping as Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer
from core.service.wizard.util.ResponseParser import ResponseParser

_WIZARD_NAME = "regconfig"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino application registration"
_AVAILABLE_SOURCE_TYPES = ["filesystem", "docker"]
_AVAILABLE_EXEC_TYPES = ["executable", "runtime", "service"]
_AVAILABLE_RESULT_RENDERERS = ["console", "file"]


class RegistrationConfigWizard(AbstractWizard):

    def __init__(self, wizard_result_transformer: AbstractWizardResultTransformer,
                 wizard_result_console_renderer: WizardResultConsoleRenderer,
                 wizard_result_file_renderer: WizardResultFileRenderer,
                 response_parser: ResponseParser):
        super().__init__(response_parser, _WIZARD_NAME, _WIZARD_DESCRIPTION)
        self._wizard_result_transformer: AbstractWizardResultTransformer = wizard_result_transformer
        self._wizard_result_console_renderer = wizard_result_console_renderer
        self._wizard_result_file_renderer = wizard_result_file_renderer

    def _init_wizard(self) -> None:

        # steps
        ws_registration_name = BaseWizardStep(Mapping.REGISTRATION_NAME, "Specify an identifier for the registration (e.g. abbreviation of app)")
        ws_source_type = OptionSelectorWizardStep(Mapping.SOURCE_TYPE, "Application will be filesystem or Docker based?", _AVAILABLE_SOURCE_TYPES)
        ws_exec_type = OptionSelectorWizardStep(Mapping.EXEC_TYPE, "Specify the execution type", _AVAILABLE_EXEC_TYPES)
        ws_home = BaseWizardStep(Mapping.SOURCE_HOME, "What will be the home directory of the application?")
        ws_binary_name = BaseWizardStep(Mapping.BINARY_NAME, "What will be the name of the binary?")
        ws_runtime_name = BaseWizardStep(Mapping.RUNTIME_NAME, "Specify the name of the runtime the app should be executed with")
        ws_command_name = BaseWizardStep(Mapping.EXEC_COMMAND_NAME, "What will be the (service) command to execute app with?")
        ws_exec_user = BaseWizardStep(Mapping.EXEC_USER, "What system user will execute the app?")
        ws_exec_args = MultiAnswerWizardStepDecorator(BaseWizardStep(Mapping.EXEC_ARGS, "Specify execution arguments (one at a line, empty line to stop)"))
        ws_health_check = OptionSelectorWizardStep(Mapping.HEALTH_CHECK_ENABLE, "Do you want to execute health check after starting the app up?")
        ws_hc_delay = BaseWizardStep(Mapping.HEALTH_CHECK_DELAY, "Specify delay between first and subsequent health checks (in Node.js 'ms' library format)")
        ws_hc_timeout = BaseWizardStep(Mapping.HEALTH_CHECK_TIMEOUT, "Specify timeout of health check requests (in Node.js 'ms' library format)")
        ws_hc_max_attempts = BaseWizardStep(Mapping.HEALTH_CHECK_MAX_ATTEMPTS, "Specify max number of health check attempts")
        ws_hc_endpoint = BaseWizardStep(Mapping.HEALTH_CHECK_ENDPOINT, "Specify the app's health check endpoint")
        ws_result_rendering = OptionSelectorWizardStep(Mapping.RESULT_RENDERING, "Write result to", _AVAILABLE_RESULT_RENDERERS)

        source_type_field = Mapping.SOURCE_TYPE.get_wizard_field()
        exec_type_field = Mapping.EXEC_TYPE.get_wizard_field()
        health_check_enable_field = Mapping.HEALTH_CHECK_ENABLE.get_wizard_field()

        # transitions
        ws_registration_name.add_transition(ws_source_type)
        ws_source_type.add_transition(ws_exec_type, lambda context: context[source_type_field] == _AVAILABLE_SOURCE_TYPES[0])
        ws_exec_type.add_transition(ws_home)
        ws_home.add_transition(ws_binary_name)
        ws_binary_name.add_transition(ws_runtime_name, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[1])
        ws_binary_name.add_transition(ws_command_name, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[2])
        ws_binary_name.add_transition(ws_exec_user, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[0])
        ws_runtime_name.add_transition(ws_exec_user)
        ws_exec_user.add_transition(ws_exec_args)
        ws_exec_args.add_transition(ws_health_check)
        ws_command_name.add_transition(ws_health_check)
        ws_health_check.add_transition(ws_hc_delay, lambda context: context[health_check_enable_field] == "yes")
        ws_health_check.add_transition(ws_result_rendering)
        ws_hc_delay.add_transition(ws_hc_timeout)
        ws_hc_timeout.add_transition(ws_hc_max_attempts)
        ws_hc_max_attempts.add_transition(ws_hc_endpoint)
        ws_hc_endpoint.add_transition(ws_result_rendering)

        self.set_entry_point(ws_registration_name)

    def _handle_result(self, result: dict) -> None:

        transformed_result: dict = self._wizard_result_transformer.transform(result)
        if result[Mapping.RESULT_RENDERING.get_wizard_field()] == _AVAILABLE_RESULT_RENDERERS[0]:
            self._wizard_result_console_renderer.render(transformed_result)
        else:
            self._wizard_result_file_renderer.render(transformed_result, lambda res: res["domino"]["registrations"])
