from typing import List

from textual import on
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Switch, Select

from domino_cli.core.service.wizard.transformer.CoordinatorConfigWizardResultTransformer import \
    CoordinatorConfigWizardResultTransformer
from domino_cli.core.tui.modals.wizards.CommonConfigWizardModal import CommonConfigWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import ConfigType


class CoordinatorConfigWizardModal(CommonConfigWizardModal):

    encryption_enabled = reactive(False, init=False)
    current_auth_mode = reactive("direct", init=False)
    configure_first_agent = reactive(False, init=False)

    def __init__(self, transformer: CoordinatorConfigWizardResultTransformer):
        super().__init__(ConfigType.COORDINATOR, transformer)

    def _get_title(self) -> Label:
        return Label("Domino Platform Coordinator (DPC) configuration wizard")

    def _add_inputs(self) -> List[Widget]:
        return [
            *self._group("Server configuration", "Configuration parameters for Domino's internal web server.", [
                self._text_input("server_context_path", "Server context path", "Root path of the API. Defaults to /.", default_value="/"),
                self._text_input("server_host", "Server host address", "Host address on which Domino should listen. Specify 0.0.0.0 to listen on all addresses. Defaults to localhost.", default_value="localhost"),
                self._text_input("server_port", "Server port", "Port on which Domino should listen. Defaults to 9987.", default_value="9987")
            ]),
            *self._group("Database configuration", "Configuration parameters for Domino's SQLite storage for deployment definitions.", [
                self._text_input("datasource_sqlite_datafile_path", "SQLite datafile path", "Defines the path of the SQLite data file. Defaults to ./data/database.sqlite.", default_value="./data/database.sqlite"),
                self._switch_input("datasource_enable_auto_import", "Enable deployment auto-import", "Enables automatically importing the YAML based deployment definitions. Requires a deployments file (see Coordinator installer)", default_value=True)
            ]),
            *self._group("Encryption configuration", "Encryption configuration for DSM (Domino Secret Manager).", [
                self._switch_input("encryption_enable", "Enable encryption in DSM", "Enabled/disable encryption-at-rest of stored secrets."),
                self._text_input("encryption_private_key", "Private RSA key path", "Path of the private RSA key for decryption.",
                                 control_group="encryption", disabled=True),
                self._text_input("encryption_public_key", "Public RSA key path", "Path of the public RSA key for encryption.",
                                 control_group="encryption", disabled=True)
            ]),
            *self._group("Logging configuration", "Controls how Coordinator will publish its logs.", [
                self._select_input("logging_min_level", "Minimum log level", "Minimum logging level, can be debug, info, warn, error.", [
                    ("Debug", "debug"),
                    ("Info", "info"),
                    ("Warn", "warn"),
                    ("Error", "error"),
                ]),
                self._switch_input("logging_json", "Enable JSON logging", "Enables formatting log messages as JSON text for more convenient log processing.")
            ]),
            *self._group("Authorization configuration", "Configuring direct or OAuth (JWT token) based authorization.", [
                self._select_input("auth_mode", "Authorization mode", "Active authorization mode. Defaults to \"direct\", which is the legacy behavior, using JWT access tokens requested from Domino. Set to \"oauth\" to change to external OAuth 2.0 Authorization Server based authorization.", [
                    ("Direct authorization (with local root account)", "direct"),
                    ("OAuth 2.0 Authorization Server based authorization", "oauth")
                ]),
                self._text_input("auth_expiration", "JWT expiration time", "Access token expiration in ms utility compatible format (e.g. 3h, 1 day, etc).",
                                 control_group="auth_direct"),
                self._text_input("auth_jwt_private_key", "JWT private key", "JWT signing private key (HMAC SHA encrypting is used).",
                                 control_group="auth_direct"),
                self._text_input("auth_username", "Local root account username", "Domino management account username.",
                                 control_group="auth_direct"),
                self._text_input("auth_password", "Local root account password", "Domino management account password. Password will be encrypted in the result.",
                                 control_group="auth_direct"),
                self._text_input("auth_oauth_issuer", "OAuth issuer", "OAuth 2.0 Authorization Server address for access token verification. (Optional, used only in \"oauth\" authorization mode.)",
                                 control_group="auth_oauth", disabled=True),
                self._text_input("auth_oauth_audience", "OAuth audience", "OAuth audience value of Domino. (Optional, used only in \"oauth\" authorization mode.)",
                                 control_group="auth_oauth", disabled=True)
            ]),
            *self._group("Agent configuration", "Configuration parameters of agent-to-Coordinator communication channels, and agent registration.", [
                self._text_input("agent_operation_timeout", "Agent operation timeout", "Specifies the interval for the agents to respond with for an operation request. (in ms utility compatible format)"),
                self._text_input("agent_api_key", "Agent API key", "API key for the agents to authorize themselves."),
                self._switch_input("agent_configure_first", "Configure your first agent?", "You can configure your first Domino Platform Agent. More agents can be added in the configuration later."),
                self._text_input("agent_host_id", "Agent host ID", "Arbitrary ID of the host the agent is running on.",
                                 control_group="first_agent", disabled=True),
                self._select_input("agent_type", "Agent type", "Type of agent, can be DOCKER or FILESYSTEM.", [
                    ("The agent will manage Docker containers", "docker"),
                    ("The agent will manage binary executable applications", "filesystem")
                ], control_group="first_agent", disabled=True),
                self._text_input("agent_key", "Agent identifier key", "Arbitrary key for the agent to distinguish itself from other agents.",
                                 control_group="first_agent", disabled=True)
            ]),
            *self._group("Coordinator info configuration", "Self-identification parameters. Can be used to distinguish instances of Domino Coordinator, if multiple installed.",[
                self._text_input("info_app_name", "Reported application name", "Full application display name.", default_value="Domino Coordinator Production"),
                self._text_input("info_abbreviation", "Reported application abbreviation", "Application name abbreviation.", default_value="DPC-PROD")
            ])
        ]

    @on(Switch.Changed, "#encryption_enable")
    def _on_encryption_enabled_changed(self, event: Switch.Changed) -> None:
        self.encryption_enabled = event.value

    def watch_encryption_enabled(self, enabled: bool) -> None:
        self._update_control_group_status(".encryption", enabled)

    @on(Select.Changed, "#auth_mode")
    def _on_auth_mode_changed(self, event: Select.Changed) -> None:
        self.current_auth_mode = event.value

    def watch_current_auth_mode(self, new_value: str) -> None:
        is_direct = new_value == "direct"
        self._update_control_group_status(".auth_direct", is_direct)
        self._update_control_group_status(".auth_oauth", not is_direct)

    @on(Switch.Changed, "#agent_configure_first")
    def _on_agent_configure_first_changed(self, event: Switch.Changed) -> None:
        self.configure_first_agent = event.value

    def watch_configure_first_agent(self, enabled: bool) -> None:
        self._update_control_group_status(".first_agent", enabled)
