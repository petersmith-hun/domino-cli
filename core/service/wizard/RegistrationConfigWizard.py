from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.RegConfigWizardDataMapping import RegConfigWizardDataMapping as Mapping
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer


class RegistrationConfigWizard(AbstractWizard):

    def __init__(self, wizard_result_transformer: AbstractWizardResultTransformer):
        super().__init__("registration_config")
        self._wizard_result_transformer = wizard_result_transformer

    def _init_wizard(self) -> None:

        # steps
        ws_registration_name = BaseWizardStep(Mapping.REGISTRATION_NAME, "Specify an identifier for the registration (e.g. abbreviation of app)")
        ws_source_type = OptionSelectorWizardStep(Mapping.SOURCE_TYPE, "Application will be filesystem or Docker based?", ["filesystem", "docker"])
        ws_exec_type = OptionSelectorWizardStep(Mapping.EXEC_TYPE, "Specify the execution type", ["executable", "runtime", "service"])
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

        source_type_field = Mapping.SOURCE_TYPE.get_wizard_field()
        exec_type_field = Mapping.EXEC_TYPE.get_wizard_field()
        health_check_enable_field = Mapping.HEALTH_CHECK_ENABLE.get_wizard_field()

        # transitions
        ws_registration_name.add_transition(ws_source_type)
        ws_source_type.add_transition(ws_exec_type, lambda context: context[source_type_field] == "filesystem")
        ws_exec_type.add_transition(ws_home)
        ws_home.add_transition(ws_binary_name)
        ws_binary_name.add_transition(ws_runtime_name, lambda context: context[exec_type_field] == "runtime")
        ws_binary_name.add_transition(ws_command_name, lambda context: context[exec_type_field] == "service")
        ws_binary_name.add_transition(ws_exec_user, lambda context: context[exec_type_field] == "executable")
        ws_runtime_name.add_transition(ws_exec_user)
        ws_exec_user.add_transition(ws_exec_args)
        ws_exec_args.add_transition(ws_health_check)
        ws_command_name.add_transition(ws_health_check)
        ws_health_check.add_transition(ws_hc_delay, lambda context: context[health_check_enable_field] == "yes")
        ws_hc_delay.add_transition(ws_hc_timeout)
        ws_hc_timeout.add_transition(ws_hc_max_attempts)
        ws_hc_max_attempts.add_transition(ws_hc_endpoint)

        self.set_entry_point(ws_registration_name)

    def _handle_result(self, result: dict):

        print("Copy the YAML document below under domino.registrations section in your Domino instance's registrations configuration file\n\n")
        print("# -- {0} registration --".format(result["reg_name"]))
        print(self._wizard_result_transformer.transform(result))
