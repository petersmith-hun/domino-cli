from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.DockerAgentConfigWizardDataMapping import Mapping as Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_WIZARD_NAME = "docker-agent"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino Platform Docker Agent configuration"
_AVAILABLE_LOGGING_LEVELS = ["debug", "info", "warn", "error"]
_AVAILABLE_AGENT_TYPES = ["docker", "filesystem"]
_AVAILABLE_DOCKER_CONNECTION_TYPES = ["socket", "tcp"]
_AVAILABLE_RESULT_RENDERERS = ["console", "file"]


class DockerAgentConfigWizard(AbstractWizard):
    """
    AbstractWizard implementation for creating Domino Platform Docker Agent configurations.
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
        ws_coordinator_host = BaseWizardStep(Mapping.COORDINATOR_HOST, "Specify Coordinator host", "ws://127.0.0.1:9987/agent")
        ws_coordinator_api_key = BaseWizardStep(Mapping.COORDINATOR_API_KEY, "Specify Coordinator API key")
        ws_coordinator_ping = BaseWizardStep(Mapping.COORDINATOR_PING, "Specify keep-alive ping interval (in Node.js 'ms' library format)")
        ws_coordinator_pong = BaseWizardStep(Mapping.COORDINATOR_PONG, "Specify keep-alive pong (ping response) timeout (in Node.js 'ms' library format)")

        ws_identification_host_id = BaseWizardStep(Mapping.IDENTIFICATION_HOST_ID, "Specify agent host ID")
        ws_identification_type = OptionSelectorWizardStep(Mapping.IDENTIFICATION_TYPE, "Select agent type", _AVAILABLE_AGENT_TYPES)
        ws_identification_key = BaseWizardStep(Mapping.IDENTIFICATION_AGENT_KEY, "Specify agent key")

        ws_logging_min_level = OptionSelectorWizardStep(Mapping.LOGGING_MIN_LEVEL, "Select minimum logging level", _AVAILABLE_LOGGING_LEVELS)
        ws_logging_enable_json = OptionSelectorWizardStep(Mapping.LOGGING_JSON, "Enable JSON logging?")

        ws_docker_connection_type = OptionSelectorWizardStep(Mapping.DOCKER_CONNECTION_TYPE, "Select Docker connection mode", _AVAILABLE_DOCKER_CONNECTION_TYPES)
        ws_docker_connection_uri_tcp = BaseWizardStep(Mapping.DOCKER_CONNECTION_URI, "Specify TCP connection URI", "http://localhost:2375")
        ws_docker_connection_uri_socket = BaseWizardStep(Mapping.DOCKER_CONNECTION_URI, "Specify UNIX socket connection URI", "/var/run/docker.sock")
        ws_docker_configure_first_registry = OptionSelectorWizardStep(Mapping.DOCKER_CONFIGURE_FIRST, "Do you want to configure your first Docker Registry now?")
        ws_docker_registry_host = BaseWizardStep(Mapping.DOCKER_SERVER_HOST, "Specify Registry host")
        ws_docker_registry_username = BaseWizardStep(Mapping.DOCKER_SERVER_USERNAME, "Specify Registry username", "")
        ws_docker_registry_password = BaseWizardStep(Mapping.DOCKER_SERVER_PASSWORD, "Specify Registry password", "")

        ws_result_rendering = OptionSelectorWizardStep(Mapping.RESULT_RENDERING, "Write result to", _AVAILABLE_RESULT_RENDERERS)

        docker_connection_type_field = Mapping.DOCKER_CONNECTION_TYPE.get_wizard_field()
        docker_first_server_field = Mapping.DOCKER_CONFIGURE_FIRST.get_wizard_field()

        # transitions
        ws_coordinator_host.add_transition(ws_coordinator_api_key)
        ws_coordinator_api_key.add_transition(ws_coordinator_ping)
        ws_coordinator_ping.add_transition(ws_coordinator_pong)
        ws_coordinator_pong.add_transition(ws_identification_host_id)

        ws_identification_host_id.add_transition(ws_identification_type)
        ws_identification_type.add_transition(ws_identification_key)
        ws_identification_key.add_transition(ws_logging_min_level)

        ws_logging_min_level.add_transition(ws_logging_enable_json)
        ws_logging_enable_json.add_transition(ws_docker_connection_type)

        ws_docker_connection_type.add_transition(ws_docker_connection_uri_socket, lambda context: context[docker_connection_type_field] == _AVAILABLE_DOCKER_CONNECTION_TYPES[0])
        ws_docker_connection_type.add_transition(ws_docker_connection_uri_tcp, lambda context: context[docker_connection_type_field] == _AVAILABLE_DOCKER_CONNECTION_TYPES[1])
        ws_docker_connection_uri_socket.add_transition(ws_docker_configure_first_registry)
        ws_docker_connection_uri_tcp.add_transition(ws_docker_configure_first_registry)

        ws_docker_configure_first_registry.add_transition(ws_docker_registry_host, lambda context: context[docker_first_server_field] == "yes")
        ws_docker_configure_first_registry.add_transition(ws_result_rendering, lambda context: context[docker_first_server_field] == "no")
        ws_docker_registry_host.add_transition(ws_docker_registry_username)
        ws_docker_registry_username.add_transition(ws_docker_registry_password)
        ws_docker_registry_password.add_transition(ws_result_rendering)

        self.set_entry_point(ws_coordinator_host)

    def _handle_result(self, result: dict) -> None:

        transformed_result: dict = self._wizard_result_transformer.transform(result)
        if result[Mapping.RESULT_RENDERING.get_wizard_field()] == _AVAILABLE_RESULT_RENDERERS[0]:
            self._wizard_result_console_renderer.render(transformed_result)
        else:
            self._wizard_result_file_renderer.render(transformed_result, lambda res: res["domino"])
