from typing import List

from textual.widget import Widget

from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer
from domino_cli.core.tui.modals.wizards.CommonConfigWizardModal import CommonConfigWizardModal
from domino_cli.core.tui.modals.wizards.WizardResultModal import ConfigType


class CommonAgentConfigWizardModal(CommonConfigWizardModal):

    def __init__(self, config_type: ConfigType, abstract_wizard_result_transformer: AbstractWizardResultTransformer):
        super().__init__(config_type, abstract_wizard_result_transformer)

    def _add_inputs(self) -> List[Widget]:
        return [
            *self._group("Coordinator connection configuration", "Configuration parameters to define how the agent can communicate with Coordinator.", [
                self._text_input("coordinator_host", "Coordinator host address", "Domino Coordinator API host address. The agent will open a WebSocket connection to this address, must start with ws:// or wss:// and end with /agent (Domino Coordinator exposes this path for the agents to connect.)"),
                self._text_input("coordinator_api_key", "Coordinator agent access API key", "API key to be used for authenticating with the Domino Coordinator."),
                self._text_input("coordinator_ping", "Agent-to-Coordinator ping interval", "Interval of the agent to ping Coordinator to keep the connection alive (in ms time string format, e.g. 2 minutes, 30s, etc)."),
                self._text_input("coordinator_pong", "Coordinator-to-Agent pong interval", "Maximum wait time for ping to be confirmed by Coordinator (in ms time string format)."),
            ]),
            *self._group("Agent identification configuration", "Agent self-identification parameters.", [
                self._text_input("identification_host_id", "Agent host ID", "Arbitrary ID of the host the agent is running on."),
                self._select_input("identification_type", "Agent type", "Type of agent, can be DOCKER or FILESYSTEM.", self._available_agent_types()),
                self._text_input("identification_agent_key", "Agent identifier key", "Arbitrary key for the agent to distinguish itself from other agents.")
            ]),
            *self._group("Logging configuration", "Controls how the agent will publish its logs.", [
                self._select_input("logging_min_level", "Minimum log level", "Minimum logging level, can be debug, info, warn, error.", [
                    ("Debug", "debug"),
                    ("Info", "info"),
                    ("Warn", "warn"),
                    ("Error", "error"),
                ]),
                self._switch_input("logging_json", "Enable JSON logging", "Enables formatting log messages as JSON text for more convenient log processing.")
            ])
        ]

    def _available_agent_types(self) -> list[tuple[str, str]]:
        return []
