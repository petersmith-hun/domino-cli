from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.DeploymentConfigWizardDataMapping import DeploymentConfigWizardDataMapping as Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.KeyValuePairAnswerWizardStep import KeyValuePairAnswerWizardStep
from core.service.wizard.step.MultiAnswerWizardStep import MultiAnswerWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_WIZARD_NAME = "deployment"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino application deployment"
_AVAILABLE_SOURCE_TYPES = ["filesystem", "docker"]
_AVAILABLE_EXEC_TYPES = ["executable", "runtime", "service"]
_AVAILABLE_DOCKER_EXEC_TYPES = ["standard"]
_AVAILABLE_RESULT_RENDERERS = ["console", "file"]
_AVAILABLE_RESTART_POLICIES = ["no", "on-failure", "always", "unless-stopped"]


class DeploymentConfigWizard(AbstractWizard):
    """
    AbstractWizard implementation for creating Domino application registration configurations.
    """
    def __init__(self, wizard_result_transformer: AbstractWizardResultTransformer,
                 wizard_result_console_renderer: WizardResultConsoleRenderer,
                 wizard_result_file_renderer: WizardResultFileRenderer):
        super().__init__(_WIZARD_NAME, _WIZARD_DESCRIPTION)
        self._wizard_result_transformer: AbstractWizardResultTransformer = wizard_result_transformer
        self._wizard_result_console_renderer: WizardResultConsoleRenderer = wizard_result_console_renderer
        self._wizard_result_file_renderer: WizardResultFileRenderer = wizard_result_file_renderer

    def _init_wizard(self) -> None:

        # steps
        ws_deployment_name = BaseWizardStep(Mapping.DEPLOYMENT_NAME, "Specify an identifier for the deployment (e.g. abbreviation of app)")
        ws_source_type = OptionSelectorWizardStep(Mapping.SOURCE_TYPE, "Application will be filesystem or Docker based?", _AVAILABLE_SOURCE_TYPES)
        ws_target_hosts = MultiAnswerWizardStep(Mapping.TARGET_HOSTS, "Hosts to deploy application to (host IDs)")
        ws_exec_type = OptionSelectorWizardStep(Mapping.EXEC_TYPE, "Specify the execution type", _AVAILABLE_EXEC_TYPES)
        ws_exec_type_docker = OptionSelectorWizardStep(Mapping.EXEC_TYPE, "Specify the Docker execution type", _AVAILABLE_DOCKER_EXEC_TYPES)
        ws_home = BaseWizardStep(Mapping.SOURCE_HOME, "What will be the home directory of the application?")
        ws_image_home = BaseWizardStep(Mapping.SOURCE_HOME, "Where will be the image located?")
        ws_binary_name = BaseWizardStep(Mapping.BINARY_NAME, "What will be the name of the binary?")
        ws_image_name = BaseWizardStep(Mapping.BINARY_NAME, "What will be the name of the image?")
        ws_runtime_name = BaseWizardStep(Mapping.RUNTIME_NAME, "Specify the name of the runtime the app should be executed with")
        ws_command_name = BaseWizardStep(Mapping.EXEC_COMMAND_NAME, "What will be the (service) command to execute app with?")
        ws_container_name = BaseWizardStep(Mapping.EXEC_COMMAND_NAME, "What will be the name of the container?")
        ws_exec_user = BaseWizardStep(Mapping.EXEC_USER, "What system user will execute the app?")
        ws_exec_args = MultiAnswerWizardStep(Mapping.EXEC_ARGS, "Specify execution arguments")
        ws_exec_args_docker_ports = KeyValuePairAnswerWizardStep(Mapping.EXEC_ARGS_DOCKER_PORTS, "Specify the ports to be exposed")
        ws_exec_args_docker_env = KeyValuePairAnswerWizardStep(Mapping.EXEC_ARGS_DOCKER_ENV, "Specify environment variables and their values")
        ws_exec_args_docker_volumes = KeyValuePairAnswerWizardStep(Mapping.EXEC_ARGS_DOCKER_VOLUMES, "Specify volume mappings")
        ws_exec_args_docker_network = BaseWizardStep(Mapping.EXEC_ARGS_DOCKER_NETWORK, "Specify network mode")
        ws_exec_args_docker_restart = OptionSelectorWizardStep(Mapping.EXEC_ARGS_DOCKER_RESTART, "Select restart policy", _AVAILABLE_RESTART_POLICIES)
        ws_exec_args_docker_cmd = MultiAnswerWizardStep(Mapping.EXEC_ARGS_DOCKER_CMD, "Specify command line arguments")
        ws_health_check = OptionSelectorWizardStep(Mapping.HEALTH_CHECK_ENABLE, "Do you want to execute health check after starting the app up?")
        ws_hc_delay = BaseWizardStep(Mapping.HEALTH_CHECK_DELAY, "Specify delay between first and subsequent health checks (in Node.js 'ms' library format)")
        ws_hc_timeout = BaseWizardStep(Mapping.HEALTH_CHECK_TIMEOUT, "Specify timeout of health check requests (in Node.js 'ms' library format)")
        ws_hc_max_attempts = BaseWizardStep(Mapping.HEALTH_CHECK_MAX_ATTEMPTS, "Specify max number of health check attempts")
        ws_hc_endpoint = BaseWizardStep(Mapping.HEALTH_CHECK_ENDPOINT, "Specify the app's health check endpoint")
        ws_info_enable = OptionSelectorWizardStep(Mapping.INFO_ENABLE, "Do you want to specify the application's info endpoint?")
        ws_info_endpoint = BaseWizardStep(Mapping.INFO_ENDPOINT, "Specify the app's info endpoint")
        ws_info_field_mapping = KeyValuePairAnswerWizardStep(Mapping.INFO_FIELD_MAPPING, "Specify the response mapping as target-source pairs (see Domino's documentation for more information)")
        ws_result_rendering = OptionSelectorWizardStep(Mapping.RESULT_RENDERING, "Write result to", _AVAILABLE_RESULT_RENDERERS)

        source_type_field = Mapping.SOURCE_TYPE.get_wizard_field()
        exec_type_field = Mapping.EXEC_TYPE.get_wizard_field()
        health_check_enable_field = Mapping.HEALTH_CHECK_ENABLE.get_wizard_field()
        info_enable_field = Mapping.INFO_ENABLE.get_wizard_field()

        # transitions
        ws_deployment_name.add_transition(ws_target_hosts)
        ws_target_hosts.add_transition(ws_source_type)
        ws_source_type.add_transition(ws_exec_type, lambda context: context[source_type_field] == _AVAILABLE_SOURCE_TYPES[0])
        ws_source_type.add_transition(ws_exec_type_docker, lambda context: context[source_type_field] == _AVAILABLE_SOURCE_TYPES[1])
        ws_exec_type.add_transition(ws_home)
        ws_home.add_transition(ws_binary_name)
        ws_binary_name.add_transition(ws_runtime_name, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[1])
        ws_binary_name.add_transition(ws_command_name, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[2])
        ws_binary_name.add_transition(ws_exec_user, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[0])
        ws_runtime_name.add_transition(ws_exec_user)
        ws_command_name.add_transition(ws_exec_user)
        ws_exec_user.add_transition(ws_health_check, lambda context: context[exec_type_field] == _AVAILABLE_EXEC_TYPES[2])
        ws_exec_user.add_transition(ws_exec_args)
        ws_exec_args.add_transition(ws_health_check)

        ws_exec_type_docker.add_transition(ws_image_home)
        ws_image_home.add_transition(ws_image_name)
        ws_image_name.add_transition(ws_container_name)
        ws_container_name.add_transition(ws_exec_args_docker_ports)
        ws_exec_args_docker_ports.add_transition(ws_exec_args_docker_env)
        ws_exec_args_docker_env.add_transition(ws_exec_args_docker_volumes)
        ws_exec_args_docker_volumes.add_transition(ws_exec_args_docker_network)
        ws_exec_args_docker_network.add_transition(ws_exec_args_docker_restart)
        ws_exec_args_docker_restart.add_transition(ws_exec_args_docker_cmd)
        ws_exec_args_docker_cmd.add_transition(ws_health_check)

        ws_health_check.add_transition(ws_hc_delay, lambda context: context[health_check_enable_field] == "yes")
        ws_health_check.add_transition(ws_info_enable)
        ws_hc_delay.add_transition(ws_hc_timeout)
        ws_hc_timeout.add_transition(ws_hc_max_attempts)
        ws_hc_max_attempts.add_transition(ws_hc_endpoint)
        ws_hc_endpoint.add_transition(ws_info_enable)

        ws_info_enable.add_transition(ws_info_endpoint, lambda context: context[info_enable_field] == "yes")
        ws_info_enable.add_transition(ws_result_rendering)
        ws_info_endpoint.add_transition(ws_info_field_mapping)
        ws_info_field_mapping.add_transition(ws_result_rendering)

        self.set_entry_point(ws_deployment_name)

    def _handle_result(self, result: dict) -> None:

        transformed_result: dict = self._wizard_result_transformer.transform(result)
        if result[Mapping.RESULT_RENDERING.get_wizard_field()] == _AVAILABLE_RESULT_RENDERERS[0]:
            self._wizard_result_console_renderer.render(transformed_result)
        else:
            self._wizard_result_file_renderer.render(transformed_result, lambda res: res["domino"]["deployments"])
