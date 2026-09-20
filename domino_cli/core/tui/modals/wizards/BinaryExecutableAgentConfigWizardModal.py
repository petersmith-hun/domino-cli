from typing import List

from textual import on
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Switch

from domino_cli.core.service.wizard.transformer.BinaryExecutableAgentConfigWizardResultTransformer import \
    BinaryExecutableAgentConfigWizardResultTransformer
from domino_cli.core.tui.modals.wizards.CommonAgentConfigWizardModal import CommonAgentConfigWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import ConfigType


class BinaryExecutableAgentConfigWizardModal(CommonAgentConfigWizardModal):

    default_socket_path = "/var/run/docker.sock"
    default_tcp_endpoint = "http://localhost:2375"

    configure_first_runtime = reactive(False, init=False)

    def __init__(self):
        super().__init__(ConfigType.BINARY_EXECUTABLE, BinaryExecutableAgentConfigWizardResultTransformer()) # TODO should be injected

    def _get_title(self) -> Label:
        return Label("Domino Platform Binary Executable Agent (DPBEA) configuration wizard")

    def _add_inputs(self) -> List[Widget]:
        return [
            *super()._add_inputs(),
            *self._group("Spawn control configuration", "Control how the applications should be spawned.", [
                self._select_input("spawn_control_service_handler", "Service handler", "Service subsystem to be used for service-based execution. Currently only systemd service subsystem is supported.", [
                    ("Systemd (Debian and Ubuntu based systems)", "systemd"),
                ]),
                self._text_input("spawn_control_start_delay", "Restart delay", "Process start delay on restart (in ms time string format, e.g. 20s, 1 minutes, etc)."),
                self._textarea_input("spawn_control_exec_users", "Allowed executor users", "List of allowed process executor users. Listed users must exist on the host system."),
            ]),
            *self._group("Storage configuration", "Controls where to store the deployments' source packages, as well as the executed application binaries.", [
                self._text_input("storage_deployments_store", "Deployment store path", "Storage path for downloaded deployment executables."),
                self._text_input("storage_app_home", "Application home path", "Application work directory root path."),
            ]),
            *self._group("Runtime configuration", "Registers the external runtimes to run RUNTIME deployments.", [
                self._switch_input("runtime_configure_first", "Configure a runtime now?", "You can configure a runtime for RUNTIME deployments. Further configurations can be added later in the configuration file."),
                self._text_input("runtime_id", "Runtime name (ID)", "Runtime internal identifier (this ID must be referenced in the deployment configuration, execution.runtime).",
                                 control_group="first_runtime", disabled=True),
                self._text_input("runtime_binary_path", "Runtime executable path", "Runtime executable path (e.g. /usr/bin/java for JRE).",
                                 control_group="first_runtime", disabled=True),
                self._text_input("runtime_healthcheck", "Runtime healthcheck command", "Runtime healthcheck command (to test if runtime exists and can run, e.g. --version).",
                                 control_group="first_runtime", disabled=True),
                self._text_input("runtime_command_line", "Runtime command line template", "Runtime command (to run the deployment, e.g. \"{args} -jar {resource}\").",
                                 control_group="first_runtime", disabled=True),
            ])
        ]

    def _available_agent_types(self) -> list[tuple[str, str]]:
        return [("The agent will manage binary executable applications", "filesystem")]

    @on(Switch.Changed, "#runtime_configure_first")
    def _on_runtime_configure_first_changed(self, event: Switch.Changed):
        self.configure_first_runtime = event.value

    def watch_configure_first_runtime(self, enabled: bool):
        self._update_control_group_status(".first_runtime", enabled)
