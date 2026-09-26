from typing import List, Callable

from textual import on
from textual.app import App
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Select, Input, Switch, LoadingIndicator

from domino_cli.core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller
from domino_cli.core.tui.modals import ConfirmationModal
from domino_cli.core.tui.modals.wizards import BaseWizardModal


class InstallerWizardModal(BaseWizardModal):

    current_component = reactive("coordinator", init=False)
    enable_deployments_file = reactive(False, init=False)
    default_config_filenames = {
        "coordinator": "coordinator_production",
        "docker-agent": "docker_agent_production",
        "binary-executable-agent": "binary_executable_agent_production"
    }

    def __init__(self, installer_resolver: Callable[[str], PlatformComponentInstaller]):
        super().__init__()
        self._installer_resolver = installer_resolver

    def _get_title(self) -> Label:
        return Label("Domino Platform component installation wizard")

    def _add_inputs(self) -> List[Widget]:

        return [
            self._select_input("component", "Platform component", "Which Domino Platform component do you want to install?",[
                ("Domino Platform Coordinator (DPC)", "coordinator"),
                ("Domino Platform Docker Agent (DPDA)", "docker-agent"),
                ("Domino Platform Binary Executable Agent (DPBEA)", "binary-executable-agent")
            ]),
            *self._group("Common settings", "These settings are applicable to all components", [
                self._text_input("configuration_filename", "Configuration filename", "Specify configuration filename without path and extension (will be used the runtime profile of the component",
                                 default_value=self.default_config_filenames[self.current_component]),
                self._text_input("config_location", "Config location", "Specify the location of the configuration file on the host (as absolute path, directory only)"),
            ]),
            *self._group("Settings for Dockerized components", "These settings are applicable to DPC and DPDA", [
                self._text_input("container_name", "Application container name", "Specify the name of the container the component will be running as", control_group="dockerized"),
                self._text_input("network_mode", "Network mode", "Specify the container's Docker network mode", default_value="host", control_group="dockerized"),
            ]),
            *self._group("Coordinator-only settings", "These settings are applicable to DPC only", [
                self._text_input("host_port", "Host port", "Specify container port to expose to host", default_value="9987", control_group="dpc"),
                self._switch_input("enable_deployments_file", "Enable deployments file", "Do you want to use static deployment configuration?", control_group="dpc"),
                self._text_input("deployments_filename", "Deployments filename", "Specify deployments configuration filename without path and extension",
                                 default_value="deployments_production", control_group="dpc", disabled=True),
                self._text_input("sqlite_location", "SQLite location", "Specify the location of the SQLite datafile on the host (as absolute path, directory only)", control_group="dpc"),
                self._text_input("encryption_keys_location", "Encryption keys location", "Specify the location of the RSA encryption key pair on the host (as absolute path, directory only)", control_group="dpc"),
            ]),
            *self._group("Binary Executable Agent only settings", "These settings are applicable to DPBEA only", [
                self._text_input("target_binary_location", "Target binary location", "Specify binary target location on host (as absolute path, DPBEA will be installed here)", control_group="dpbea", disabled=True),
            ])
        ]

    @on(Select.Changed, "#component")
    def _on_source_type_changed(self, event: Select.Changed) -> None:
        self.current_component = event.value

    def watch_current_component(self, new_value: str) -> None:
        is_dpc = new_value == "coordinator"
        is_dpda = new_value == "docker-agent"
        is_dpbea = new_value == "binary-executable-agent"

        self._update_control_group_status(".dockerized", is_dpc or is_dpda)
        self._update_control_group_status(".dpc", is_dpc)
        self._update_control_group_status(".dpbea", is_dpbea)
        self.query_one("#configuration_filename", Input).value = self.default_config_filenames[new_value]

    @on(Switch.Changed, "#enable_deployments_file")
    def _on_enable_deployments_file_changed(self, event: Switch.Changed) -> None:
        self.enable_deployments_file = event.value

    def watch_enable_deployments_file(self, new_value: bool) -> None:
        self.query_one("#deployments_filename", Input).disabled = not new_value

    def _handle_result(self, responses: dict[str, str | list[str]]) -> None:
        self.app.push_screen(ConfirmationModal(f"The wizard will now install the {self.current_component} component", lambda :self._do_install(responses)))

    def _do_install(self, responses: dict[str, str | list[str]]) -> None:

        installer = self._installer_resolver(str(self.current_component))

        self._show_loading_indicator(self.app, True)
        self.app.run_worker(lambda: self._run_installer(self.app, installer, responses), thread=True)

    def _run_installer(self, app: App, installer: PlatformComponentInstaller, responses: dict[str, str | list[str]]) -> None:

        try:
            installer.install(responses, auto_install=True)
            app.call_from_thread(lambda: self.app.notify(f"Successfully installed {self.current_component} component", title="Installation result", severity="information"))

        except Exception as exc:
            app.call_from_thread(lambda: self.app.notify(f"Failed to install {self.current_component} component: {str(exc)}", title="Installation result", severity="error"))

        finally:
            app.call_from_thread(lambda: self._show_loading_indicator(app, False))

    def _show_loading_indicator(self, app: App, show: bool):
        app.query_one(LoadingIndicator).display = show
