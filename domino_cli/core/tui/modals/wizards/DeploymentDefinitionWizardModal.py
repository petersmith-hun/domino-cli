from typing import List

from textual import on
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Select, Switch

from domino_cli.core.service.wizard.transformer.DeploymentConfigWizardResultTransformer import \
    DeploymentConfigWizardResultTransformer
from domino_cli.core.tui.modals.wizards.CommonConfigWizardModal import CommonConfigWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import ConfigType


class DeploymentDefinitionWizardModal(CommonConfigWizardModal):

    current_source_type = reactive[str]("DOCKER", init=False)
    enable_multi_instance_options = reactive[bool](False, init=False)
    enable_health_check_options = reactive[bool](False, init=False)
    enable_info_endpoint_options = reactive[bool](False, init=False)

    docker_exec_types = [("Spin up the application via a standard Docker container", "STANDARD")]
    filesystem_exec_types = [
        ("Spin up the application directly via its executable", "EXECUTABLE"),
        ("Spin up the application with the aid of an external runtime environment", "RUNTIME"),
        ("Spin up the application via an OS service unit (init.d, systemd, etc.).", "SERVICE")
    ]

    def __init__(self, transformer: DeploymentConfigWizardResultTransformer):
        super().__init__(ConfigType.DEPLOYMENT, transformer)

    def _get_title(self) -> Label:
        return Label("Deployment definition wizard")

    def _add_inputs(self) -> List[Widget]:

        return [
            self._text_input("deployment_name", "Deployment name", "Name (primary ID) of the deployment", required=True),
            *self._group("Source configuration", "Determines where the application's executable is located and how it should be treated", [
                self._select_input("source_type", "Type", "Type of the executable. Currently FILESYSTEM and DOCKER are supported, which means either the executable is located in the server's filesystem as a standalone executable binary file or exists as a Docker container.",
                                   [("Run as Docker Container", "DOCKER"), ("Run as binary executable", "FILESYSTEM")]),
                self._text_input("src_home", "Home", "Binary source URL or Docker Registry URI.",
                                 required=True),
                self._text_input("src_bin_name", "Resource", "The name of the deployed executable.",
                                 required=True),
            ]),
            *self._group("Target configuration", "Target configuration determines the actual server instance where your application is running. You may also define some directives for deploying multiple instances of the application on different hosts.", [
                self._textarea_input("target_hosts", "Hosts", "List of arbitrary host IDs, where you would like to install your application.",
                                     required=True),
                self._switch_input("multi_instance_enable", "Multi-instance", "Enables multi-instance deployment."),
                self._text_input("instance_count", "Instance count", "Sets the number of deployed instances.", disabled=True, control_group="multi-instance"),
                self._select_input("spread_mode", "Instance spread mode", "Controls how the instances should be spread across multiple hosts.",
                                   [("Replicate all instances over hosts", "replicate"), ("One instance per host", "one-per-host")], disabled=True, control_group="multi-instance"),
                self._select_input("naming_strategy", "Instance naming strategy", "Controls how to derive the instance names of the deployment command name.",
                                   [("Incremental suffix (0-based)", "incremental-suffix"), ("Custom predefined names", "custom-predefined")], disabled=True, control_group="multi-instance"),
                self._textarea_input("defined_names", "Defined instance names", "List of the predefined custom instance names (for custom-predefined naming strategy).", disabled=True, control_group="multi-instance"),
                self._text_input("port_offset", "Port offset", "Port offset (e.g. +100, -200, etc.) to derive instance ports from the defined base port(s).", disabled=True, control_group="multi-instance"),
                self._text_input("host_network_base_port", "Host network base port", "Base port number for \"host\" Docker networking mode.", disabled=True, control_group="multi-instance")
            ]),
            *self._group("Execution configuration", "Execution parameters determine how the executable should be spun up.", [
                self._select_input("exec_type", "Execution mode", "Spin up method for the application.", self.docker_exec_types),
                self._text_input("exec_cmd_name", "Command name", "In case the application requires an explicit command to be executed to spin it up, that should be provided here (service name or Docker container name)"),
                self._textarea_input("exec_args_docker_ports", "Exposed ports", "Port mappings as a map of exposed:internal port pairs.", control_group="docker"),
                self._textarea_input("exec_args_docker_env", "Environment variables", "Environment variables to be passed to the container as map of key:value pairs", control_group="docker"),
                self._textarea_input("exec_args_docker_volumes", "Mounted volumes", "Volume mounts as source:target:ro/rw triplets.", control_group="docker"),
                self._text_input("exec_args_docker_network", "Network mode", "Network mode (host, bridge, or existing network name).", control_group="docker"),
                self._text_input("exec_args_docker_restart", "Restart policy", "Restart policy of the container. Standard parameters should be used (always, unless-stopped, on-failure[:max-retries], or no).", control_group="docker"),
                self._textarea_input("exec_args_docker_cmd", "Container command-line arguments", "Command line arguments to be passed to the container.", control_group="docker"),
                self._text_input("runtime_name", "Runtime name", "Name of a registered runtime to run application with. Used only by RUNTIME typed deployments.", True, control_group="filesystem"),
                self._text_input("exec_user", "Executor user name", "(Usually a service-only) OS user which will execute the application. A group with the same name should also exist.", True, control_group="filesystem"),
                self._textarea_input("exec_args", "Execution arguments", "List of command-line arguments to be passed to the application.", True, control_group="filesystem")
            ]),
            *self._group("Health-check configuration", "It is possible to run a health-check right after the application has been deployed and started up.", [
                self._switch_input("hc_enable", "Enable health-check", "Enables executing health-check after start."),
                self._text_input("hc_delay", "Delay", "Delay before the first and between the subsequent health-check requests. Must be provided in ms-utility format (e.g. 100ms, 20s, 1m).", True, "hc"),
                self._text_input("hc_timeout", "Timeout", "Maximum wait time for a single health-check request. Must be provided in ms-utility format.", True, "hc"),
                self._text_input("hc_max_attempts", "Max attempts", "Maximum number of health-check attempts in case of failure. In case an application exceeds this limit, it is considered dead.", True, "hc"),
                self._text_input("hc_endpoint", "Endpoint", "Health-check endpoint of the application. If present, port number will be aligned for multi-instance deployments.", True, "hc"),
            ]),
            *self._group("Application info endpoint configuration", "Deployed applications may provide information about their state via an info endpoint.", [
                self._switch_input("info_enable", "Enable info endpoint", "Enables application info endpoint."),
                self._text_input("info_endpoint", "Endpoint", "Application info endpoint URI. (Full path is needed - host, port, context path, path). If present, port number will be aligned for multi-instance deployments.", True, "info"),
                self._textarea_input("info_field_mapping", "Field mapping", "Configures how the info endpoint's response should be mapped to Domino's own response. See full documentation for examples.", True, "info"),
            ])
        ]

    @on(Select.Changed, "#source_type")
    def _on_source_type_changed(self, event: Select.Changed) -> None:
        self.current_source_type = event.value

    def watch_current_source_type(self, new_value: str) -> None:
        is_docker = new_value == "DOCKER"
        self._update_control_group_status(".docker", is_docker)
        self._update_control_group_status(".filesystem", not is_docker)
        self.query_one("#exec_type", Select).set_options(self.docker_exec_types \
            if is_docker \
            else self.filesystem_exec_types)

    @on(Switch.Changed, "#multi_instance_enable")
    def _on_multi_instance_enable_changed(self, event: Switch.Changed) -> None:
        self.enable_multi_instance_options = event.value

    def watch_enable_multi_instance_options(self, enabled: bool) -> None:
        self._update_control_group_status(".multi-instance", enabled)

    @on(Switch.Changed, "#hc_enable")
    def _on_hc_enable_changed(self, event: Switch.Changed) -> None:
        self.enable_health_check_options = event.value

    def watch_enable_health_check_options(self, enabled: bool) -> None:
        self._update_control_group_status(".hc", enabled)

    @on(Switch.Changed, "#info_enable")
    def _on_info_enable_changed(self, event: Switch.Changed) -> None:
        self.enable_info_endpoint_options = event.value

    def watch_enable_info_endpoint_options(self, enabled: bool) -> None:
        self._update_control_group_status(".info", enabled)
