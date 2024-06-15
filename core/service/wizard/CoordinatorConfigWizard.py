from core.service.wizard.AbstractWizard import AbstractWizard
from core.service.wizard.mapping.CoordinatorConfigWizardDataMapping import Mapping as Mapping
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_WIZARD_NAME = "coordinator"
_WIZARD_DESCRIPTION = "Creates a properly configured Domino Platform Coordinator configuration"
_AVAILABLE_LOGGING_LEVELS = ["debug", "info", "warn", "error"]
_AVAILABLE_AUTH_MODES = ["direct", "oauth"]
_AVAILABLE_AGENT_TYPES = ["docker", "filesystem"]
_AVAILABLE_RESULT_RENDERERS = ["console", "file"]


class CoordinatorConfigWizard(AbstractWizard):
    """
    AbstractWizard implementation for creating Domino Platform Coordinator configurations.
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
        ws_server_context_path = BaseWizardStep(Mapping.SERVER_CONTEXT_PATH, "Specify server context (base) path", "/")
        ws_server_host = BaseWizardStep(Mapping.SERVER_HOST, "Specify server host address", "0.0.0.0")
        ws_server_port = BaseWizardStep(Mapping.SERVER_PORT, "Specify server port", "9987")

        ws_logging_min_level = OptionSelectorWizardStep(Mapping.LOGGING_MIN_LEVEL, "Select minimum logging level", _AVAILABLE_LOGGING_LEVELS)
        ws_logging_enable_json = OptionSelectorWizardStep(Mapping.LOGGING_JSON, "Enable JSON logging?")

        ws_auth_mode = OptionSelectorWizardStep(Mapping.AUTH_MODE, "Select authentication mode", _AVAILABLE_AUTH_MODES)
        ws_auth_expiration = BaseWizardStep(Mapping.AUTH_EXPIRATION, "Specify JWT token expiration in (in Node.js 'ms' library format)")
        ws_auth_jwt_private_key = BaseWizardStep(Mapping.AUTH_JWT_PRIVATE_KEY, "Specify JWT private key")
        ws_auth_username = BaseWizardStep(Mapping.AUTH_USERNAME, "Specify local administrator username")
        ws_auth_password = BaseWizardStep(Mapping.AUTH_PASSWORD, "Specify local administrator password (will be encrypted in result)")
        ws_auth_oauth_issuer = BaseWizardStep(Mapping.AUTH_OAUTH_ISSUER, "Specify OAuth issuer")
        ws_auth_oauth_audience = BaseWizardStep(Mapping.AUTH_OAUTH_AUDIENCE, "Specify OAuth audience")

        ws_agent_operation_timeout = BaseWizardStep(Mapping.AGENT_OPERATION_TIMEOUT, "Specify agent operation timeout (in Node.js 'ms' library format)")
        ws_agent_api_key = BaseWizardStep(Mapping.AGENT_API_KEY, "Specify agent API key (will be encrypted in result)")
        ws_agent_configure_first_agent = OptionSelectorWizardStep(Mapping.AGENT_CONFIGURE_FIRST, "Do you want to configure your first agent now?")
        ws_agent_host_id = BaseWizardStep(Mapping.AGENT_HOST_ID, "Specify agent host ID")
        ws_agent_type = OptionSelectorWizardStep(Mapping.AGENT_TYPE, "Select agent type", _AVAILABLE_AGENT_TYPES)
        ws_agent_key = BaseWizardStep(Mapping.AGENT_AGENT_KEY, "Specify agent key")

        ws_info_app_name = BaseWizardStep(Mapping.INFO_APP_NAME, "Specify application full name", "Domino Platform Coordinator")
        ws_info_abbreviation = BaseWizardStep(Mapping.INFO_ABBREVIATION, "Specify application name abbreviation", "DPC")

        ws_result_rendering = OptionSelectorWizardStep(Mapping.RESULT_RENDERING, "Write result to", _AVAILABLE_RESULT_RENDERERS)

        auth_mode_field = Mapping.AUTH_MODE.get_wizard_field()
        agent_configuration_field = Mapping.AGENT_CONFIGURE_FIRST.get_wizard_field()

        # transitions
        ws_server_context_path.add_transition(ws_server_host)
        ws_server_host.add_transition(ws_server_port)
        ws_server_port.add_transition(ws_logging_min_level)
        ws_logging_min_level.add_transition(ws_logging_enable_json)
        ws_logging_enable_json.add_transition(ws_auth_mode)

        ws_auth_mode.add_transition(ws_auth_expiration, lambda context: context[auth_mode_field] == _AVAILABLE_AUTH_MODES[0])
        ws_auth_expiration.add_transition(ws_auth_jwt_private_key)
        ws_auth_jwt_private_key.add_transition(ws_auth_username)
        ws_auth_username.add_transition(ws_auth_password)
        ws_auth_password.add_transition(ws_agent_operation_timeout)

        ws_auth_mode.add_transition(ws_auth_oauth_issuer, lambda context: context[auth_mode_field] == _AVAILABLE_AUTH_MODES[1])
        ws_auth_oauth_issuer.add_transition(ws_auth_oauth_audience)
        ws_auth_oauth_audience.add_transition(ws_agent_operation_timeout)

        ws_agent_operation_timeout.add_transition(ws_agent_api_key)
        ws_agent_api_key.add_transition(ws_agent_configure_first_agent)
        ws_agent_configure_first_agent.add_transition(ws_agent_host_id, lambda context: context[agent_configuration_field] == "yes")
        ws_agent_host_id.add_transition(ws_agent_type)
        ws_agent_type.add_transition(ws_agent_key)
        ws_agent_key.add_transition(ws_info_app_name)

        ws_agent_configure_first_agent.add_transition(ws_info_app_name, lambda context: context[agent_configuration_field] == "no")

        ws_info_app_name.add_transition(ws_info_abbreviation)
        ws_info_abbreviation.add_transition(ws_result_rendering)

        self.set_entry_point(ws_server_context_path)

    def _handle_result(self, result: dict) -> None:

        transformed_result: dict = self._wizard_result_transformer.transform(result)
        if result[Mapping.RESULT_RENDERING.get_wizard_field()] == _AVAILABLE_RESULT_RENDERERS[0]:
            self._wizard_result_console_renderer.render(transformed_result)
        else:
            self._wizard_result_file_renderer.render(transformed_result, lambda res: res["domino"])
