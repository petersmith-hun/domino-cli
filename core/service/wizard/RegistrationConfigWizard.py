import yaml

from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep


class RegistrationConfigWizard(AbstractWizard):

    def __init__(self):
        super().__init__("registration_config")

    def _init_wizard(self) -> None:

        # steps
        ws_source_type = OptionSelectorWizardStep("source_type", "Application will be filesystem or Docker based?", ["filesystem", "docker"])
        ws_exec_type = OptionSelectorWizardStep("exec_type", "Specify the execution type", ["executable", "runtime", "service"])
        ws_home = BaseWizardStep("src_home", "What will be the home directory of the application?")
        ws_binary_name = BaseWizardStep("src_bin_name", "What will be the name of the binary?")
        ws_runtime_name = BaseWizardStep("runtime_name", "Specify the name of the runtime the app should be executed with")
        ws_command_name = BaseWizardStep("exec_cmd_name", "What will be the (service) command to execute app with?")
        ws_exec_user = BaseWizardStep("exec_user", "What system user will execute the app?")
        ws_exec_args = MultiAnswerWizardStepDecorator(BaseWizardStep("exec_args", "Specify execution arguments (one at a line, empty line to stop)"))
        ws_health_check = OptionSelectorWizardStep("hc_enable", "Do you want to execute health check after starting the app up?")
        ws_hc_delay = BaseWizardStep("hc_delay", "Specify delay between first and subsequent health checks (in Node.js 'ms' library format)")
        ws_hc_timeout = BaseWizardStep("hc_timeout", "Specify timeout of health check requests (in Node.js 'ms' library format)")
        ws_hc_max_attempts = BaseWizardStep("hc_max_attempts", "Specify max number of health check attempts")
        ws_hc_endpoint = BaseWizardStep("hc_endpoint", "Specify the app's health check endpoint")

        # transitions
        ws_source_type.add_transition(ws_exec_type, lambda context: context["source_type"] == "filesystem")
        ws_exec_type.add_transition(ws_home)
        ws_home.add_transition(ws_binary_name)
        ws_binary_name.add_transition(ws_runtime_name, lambda context: context["exec_type"] == "runtime")
        ws_binary_name.add_transition(ws_command_name, lambda context: context["exec_type"] == "service")
        ws_binary_name.add_transition(ws_exec_user, lambda context: context["exec_type"] == "executable")
        ws_runtime_name.add_transition(ws_exec_user)
        ws_exec_user.add_transition(ws_exec_args)
        ws_exec_args.add_transition(ws_health_check)
        ws_command_name.add_transition(ws_health_check)
        ws_health_check.add_transition(ws_hc_delay, lambda context: context["hc_enable"] == "yes")
        ws_hc_delay.add_transition(ws_hc_timeout)
        ws_hc_timeout.add_transition(ws_hc_max_attempts)
        ws_hc_max_attempts.add_transition(ws_hc_endpoint)

        self.set_entry_point(ws_source_type)

    def _handle_result(self, result: dict):

        # TODO reformat the dict and return it as yaml dump
        print(yaml.dump(result))

        # [print("{0}: {1}".format(key, result[key])) for key in result.keys()]
