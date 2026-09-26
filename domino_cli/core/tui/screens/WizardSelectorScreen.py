from typing import cast, Callable

from textual.containers import VerticalGroup
from textual.widgets import Label, ListView, ListItem

from domino_cli.core.tui.modals.wizards import BaseWizardModal


class WizardListItem(ListItem):

    DEFAULT_CSS = """
    WizardListItem {
        padding: 1 2;
        outline-top: none;
        outline-bottom: none;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
    }

    .wizard_name {
        text-style: bold;
    }
    
    .wizard_description {
        color: $text-muted;
        text-style: italic;
    }
    """

    def __init__(self, id: str, name: str, description: str):
        super().__init__(VerticalGroup(
            Label(name, classes="wizard_name"),
            Label(f"ⓘ {description}", classes="wizard_description")
        ))
        self.wizard_id = id


class WizardSelectorScreen(ListView):
    _documentation_base_url = "https://github.com/petersmith-hun/domino-platform/tree/master/modules/"

    DEFAULT_CSS = """
    WizardSelectorScreen {
        background: $surface;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        outline-bottom: ascii $accent;
    }
    """
    def __init__(self, modal_factory: Callable[[str], BaseWizardModal | None]):
        super().__init__(
            WizardListItem("wizard_deployment_definition",
                           "Deployment definition wizard",
                           f"Creates a new deployment definition, that can be imported into Domino. See {self._documentation_base_url}coordinator#deployments-configuration for more details."),
            WizardListItem("wizard_coordinator",
                           "Coordinator configuration wizard",
                           f"Creates a Domino Platform Coordinator (DPC) configuration. See {self._documentation_base_url}coordinator#main-configuration for more details."),
            WizardListItem("wizard_docker_agent_config",
                           "Docker Agent configuration wizard",
                           f"Creates a deployment agent configuration for a Domino Platform Docker Agent (DPDA). See {self._documentation_base_url}binary-executable-agent#configuration for more details."),
            WizardListItem("wizard_bin_exec_agent",
                           "Binary Executable Agent configuration wizard",
                           f"Creates a deployment agent configuration for a Domino Platform Binary Executable Agent (DPBEA). See {self._documentation_base_url}docker-agent#configuration for more details."),
            WizardListItem("wizard_installer",
                           "Domino Platform installer wizard",
                           "Configures and installs the Domino Platform components."),
            id="wizards")
        self._modal_factory = modal_factory

    def action_select_cursor(self) -> None:

        wizard_id = cast(WizardListItem, self.highlighted_child).wizard_id
        wizard_modal = self._modal_factory(wizard_id)

        if wizard_modal:
            self.app.push_screen(wizard_modal)

        else:
            self.app.notify("Unknown wizard selected", title="Wizard Selector", severity="error")
