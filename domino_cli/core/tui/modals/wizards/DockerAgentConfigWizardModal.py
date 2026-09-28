from typing import List

from textual import on
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Switch, Select, Input

from domino_cli.core.service.wizard.transformer.DockerAgentConfigWizardResultTransformer import \
    DockerAgentConfigWizardResultTransformer
from domino_cli.core.tui.modals.wizards.CommonAgentConfigWizardModal import CommonAgentConfigWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import ConfigType


class DockerAgentConfigWizardModal(CommonAgentConfigWizardModal):

    default_connection_uri_map = {
        "socket": "/var/run/docker.sock",
        "tcp": "http://localhost:2375"
    }

    current_connection_type = reactive("socket", init=False)
    configure_first_registry = reactive(False, init=False)

    def __init__(self, transformer: DockerAgentConfigWizardResultTransformer):
        super().__init__(ConfigType.DOCKER_AGENT, transformer)

    def _get_title(self) -> Label:
        return Label("Domino Platform Docker Agent (DPDA) configuration wizard")

    def _add_inputs(self) -> List[Widget]:
        return [
            *super()._add_inputs(),
            *self._group("Docker Engine and registry configuration", "Local Docker Engine connection parameters and application source Docker Registry access configuration.", [
                self._select_input("docker_connection_type", "Docker Engine connection type", "Type of Docker Engine connection, can be socket or tcp.", [
                    ("Connect via Unix Socket (Recommended)", "socket"),
                    ("Connect via TCP endpoint", "tcp")
                ]),
                self._text_input("docker_connection_uri", "Docker Engine connection URI", "Docker Engine server URI. Usually either /var/run/docker.sock for socket connection, or http://localhost:2375 for TCP connection.",
                                 default_value=self.default_connection_uri_map["socket"]),
                self._switch_input("docker_registry_configure_first", "Configure first Docker Registry access?", "You may configure a private Docker Registry now. Further configuration can be done later via the configuration."),
                self._text_input("docker_registry_host", "Registry host", "Docker Registry server address (with port).",
                                 control_group="first_registry", disabled=True),
                self._text_input("docker_registry_username", "Registry username", "Docker Registry server username.",
                                 control_group="first_registry", disabled=True),
                self._text_input("docker_registry_password", "Registry password", "Docker Registry server password.",
                                 control_group="first_registry", disabled=True)
            ])
        ]

    def _available_agent_types(self) -> list[tuple[str, str]]:
        return [("The agent will manage Docker containers", "docker")]

    @on(Select.Changed, "#docker_connection_type")
    def _on_connection_type_changed(self, event: Select.Changed) -> None:
        self.current_connection_type = event.value

    def watch_current_connection_type(self, current_value: str) -> None:
        self.query_one("#docker_connection_uri", Input).value = self.default_connection_uri_map[current_value]

    @on(Switch.Changed, "#docker_registry_configure_first")
    def _on_registry_configuration_changed(self, event: Switch.Changed) -> None:
        self.configure_first_registry = event.value

    def watch_configure_first_registry(self, enabled: bool) -> None:
        self._update_control_group_status(".first_registry", enabled)
