from typing import List

from requests import Response

from domino_cli.core.cli.Logging import info
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.domain.Deployments import DeploymentSummary, LifecycleResponse, Page
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoCommand import DominoRequestDescriptor
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.service.utility.APIRequestHandler import APIRequestHandler
from domino_cli.core.util.ResponseUtils import is_successful


class DominoService:
    """
    Service implementation handling command processing.
    """
    def __init__(self, domino_client: DominoClient, api_request_handler: APIRequestHandler):
        self._domino_client = domino_client
        self._api_request_handler = api_request_handler

    def execute_lifecycle_command(self, domino_command: DominoCommand, application: str, version: str | None = None, roll: bool = False, instance: str | None = None) -> LifecycleResponse | dict:
        """
        Executes the given lifecycle command for the given application.

        :param domino_command: DominoCommand object specifying the command to be executed
        :param application: application name to send the command to
        :param version: (optional) version number
        :param roll: instructs Domino to roll the application instances of multi-instance deployments
        :param instance: instructs Domino to only apply the command to a specific instance of a multi-instance deployment
        """
        query: dict[str, str] = {"roll": "true" if roll else "false"}
        if instance:
            query["instance"] = instance

        domino_request_descriptor: DominoRequestDescriptor = domino_command.value
        formatted_path = domino_request_descriptor.path_template.format(application, version)
        domino_request = DominoRequest(domino_request_descriptor.method, formatted_path, authenticated=True, query=query)

        info("Sending {0} command for application {1} via Domino".format(domino_command.name, application))

        response: Response = self._domino_client.send_command(domino_request)

        if is_successful(response):
            return response.json() \
                if domino_command == DominoCommand.INFO \
                else LifecycleResponse(response.json())
        else:
            raise DominoServiceException(response)

    def import_definition(self, optional_definition_path: str | None = None) -> None:
        """
        Imports the given deployment definition. If a path is not provided, defaults to ".domino/deployment.yml".

        :param optional_definition_path: optional path to a deployment definition
        """
        definition_path = optional_definition_path \
            if optional_definition_path \
            else ".domino/deployment.yml"
        info(f"Requesting Domino to import deployment definition from={definition_path}")

        with open(definition_path, "r") as definition_file:
            definition = definition_file.read()
            domino_request_descriptor: DominoRequestDescriptor = DominoCommand.IMPORT.value
            domino_request = DominoRequest(domino_request_descriptor.method, domino_request_descriptor.path_template,
                                           body=definition, authenticated=True, as_text=True)
            response = self._domino_client.send_command(domino_request)

            if not is_successful(response):
                raise DominoServiceException(response)

    def import_oauth_descriptor(self, application: str, dry_run: bool, optional_descriptor_path: str | None = None) -> None:
        """
        Imports the given OAuth descriptor. If a path is not provided, defaults to ".domino/oauth.yml".

        :param application: name of the application name to submit the OAuth descriptor for
        :param dry_run: do not execute actual changes (verifies the descriptor and the relations defined by it, without saving it)
        :param optional_descriptor_path: optional path to an OAuth descriptor
        """
        descriptor_path = optional_descriptor_path \
            if optional_descriptor_path \
            else ".domino/oauth.yml"
        info(f"Requesting Domino to import OAuth application descriptor from={descriptor_path}")

        with open(descriptor_path, "r") as descriptor_file:
            descriptor = descriptor_file.read()
            domino_request_descriptor: DominoRequestDescriptor = DominoCommand.IMPORT_OAUTH.value
            domino_request = DominoRequest(domino_request_descriptor.method,
                                           domino_request_descriptor.path_template.format(application),
                                           query={"dry-run": "true"} if dry_run else None,
                                           body=descriptor, authenticated=True, as_text=True)
            response = self._domino_client.send_command(domino_request)

            if not is_successful(response):
                raise DominoServiceException(response)

    def get_deployments_page(self) -> List[DeploymentSummary]:
        """
        Lists deployments.
        """
        response = self._api_request_handler.send_command(DominoCommand.LIST_DEPLOYMENTS)
        deployments_page: Page[DeploymentSummary] = self._api_request_handler.handle_response(response, lambda data: Page[DeploymentSummary](data, DeploymentSummary))

        return deployments_page.body

    @staticmethod
    def _parse_deployments_page(response: dict | List[dict] | object) -> List[DeploymentSummary]:

        if not isinstance(response, dict):
            return []

        return [DeploymentSummary(item) for item in response["body"]]

