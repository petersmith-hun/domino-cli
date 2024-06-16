from core.service.wizard.AbstractAgentConfigWizard import AbstractAgentConfigWizard
from core.service.wizard.mapping.DockerAgentConfigWizardDataMapping import Mapping as Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_WIZARD_NAME = "docker-agent"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino Platform Docker Agent configuration"
_AVAILABLE_DOCKER_CONNECTION_TYPES = ["socket", "tcp"]


class DockerAgentConfigWizard(AbstractAgentConfigWizard):
    """
    AbstractWizard implementation for creating Domino Platform Docker Agent configurations.
    """

    def __init__(self, wizard_result_transformer: AbstractWizardResultTransformer,
                 wizard_result_console_renderer: WizardResultConsoleRenderer,
                 wizard_result_file_renderer: WizardResultFileRenderer):
        super().__init__(_WIZARD_NAME, _WIZARD_DESCRIPTION,
                         wizard_result_transformer,
                         wizard_result_console_renderer,
                         wizard_result_file_renderer)

    def _chain_additional_steps(self, ws_logging_enable_json: BaseWizardStep, ws_result_rendering: BaseWizardStep) -> None:

        # steps
        ws_docker_connection_type = OptionSelectorWizardStep(Mapping.DOCKER_CONNECTION_TYPE, "Select Docker connection mode", _AVAILABLE_DOCKER_CONNECTION_TYPES)
        ws_docker_connection_uri_tcp = BaseWizardStep(Mapping.DOCKER_CONNECTION_URI, "Specify TCP connection URI", "http://localhost:2375")
        ws_docker_connection_uri_socket = BaseWizardStep(Mapping.DOCKER_CONNECTION_URI, "Specify UNIX socket connection URI", "/var/run/docker.sock")
        ws_docker_configure_first_registry = OptionSelectorWizardStep(Mapping.DOCKER_CONFIGURE_FIRST, "Do you want to configure your first Docker Registry now?")
        ws_docker_registry_host = BaseWizardStep(Mapping.DOCKER_SERVER_HOST, "Specify Registry host")
        ws_docker_registry_username = BaseWizardStep(Mapping.DOCKER_SERVER_USERNAME, "Specify Registry username", "")
        ws_docker_registry_password = BaseWizardStep(Mapping.DOCKER_SERVER_PASSWORD, "Specify Registry password", "")

        docker_connection_type_field = Mapping.DOCKER_CONNECTION_TYPE.get_wizard_field()
        docker_first_server_field = Mapping.DOCKER_CONFIGURE_FIRST.get_wizard_field()

        # transitions
        ws_logging_enable_json.add_transition(ws_docker_connection_type)

        ws_docker_connection_type.add_transition(ws_docker_connection_uri_socket, lambda context: context[docker_connection_type_field] == _AVAILABLE_DOCKER_CONNECTION_TYPES[0])
        ws_docker_connection_type.add_transition(ws_docker_connection_uri_tcp, lambda context: context[docker_connection_type_field] == _AVAILABLE_DOCKER_CONNECTION_TYPES[1])
        ws_docker_connection_uri_socket.add_transition(ws_docker_configure_first_registry)
        ws_docker_connection_uri_tcp.add_transition(ws_docker_configure_first_registry)

        ws_docker_configure_first_registry.add_transition(ws_result_rendering, lambda context: context[docker_first_server_field] == "no")
        ws_docker_configure_first_registry.add_transition(ws_docker_registry_host, lambda context: context[docker_first_server_field] == "yes")
        ws_docker_registry_host.add_transition(ws_docker_registry_username)
        ws_docker_registry_username.add_transition(ws_docker_registry_password)
        ws_docker_registry_password.add_transition(ws_result_rendering)
