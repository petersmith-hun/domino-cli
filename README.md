# Domino CLI

Domino CLI is a command line interface tool written in Python for 
[Domino Platform deployment orchestration system](https://github.com/petersmith-hun/domino-platform).
Its purpose is to provide a convenient way of controlling the Domino Platform Coordinator via its REST interface. It can 
also generate configuration files for each Domino Platform components, as well as install those.

## Requirements

* Domino CLI requires Python 3.x for execution (tested on Python 3.7, 3.8, 3.10 and 3.12).
* Pip (Python package installer) is required for installation.
* It is executable both on Windows and Linux systems.

## Configuration

The tool can be configured via the following environment variables:

| Environment variable       | Mandatory?    | Description                                                                                   |
|----------------------------|---------------|-----------------------------------------------------------------------------------------------|
| DOMINO_BASE_URL            | Yes           | URL of Domino instance to be controlled, e.g. http://localhost:8080/domino                    |
| DOMINO_CLI_USERNAME        | No            | Optional predefined username for accessing Domino                                             |
| DOMINO_CLI_PASSWORD        | No            | Optional predefined password for accessing Domino                                             |
| DOMINO_CLI_DEBUG_MODE      | No            | Optional debug switch. Currently its only effect is echoing the parsed command                |
| DOMINO_DEFAULT_AUTH_MODE   | No            | Changes how Domino CLI acquires the access token for Domino. Defaults to direct mode (legacy) |
| DOMINO_OAUTH_TOKEN_URL     | In OAuth mode | OAuth 2.0 compliant authorization server address, including the token request endpoint path   |
| DOMINO_OAUTH_CLIENT_ID     | In OAuth mode | OAuth 2.0 Client ID of Domino CLI                                                             |
| DOMINO_OAUTH_CLIENT_SECRET | In OAuth mode | OAuth 2.0 Client Secret of Domino CLI                                                         |
| DOMINO_OAUTH_SCOPE         | In OAuth mode | OAuth 2.0 access token scope                                                                  |                                                                                         
| DOMINO_OAUTH_AUDIENCE      | No            | OAuth 2.0 audience of Domino                                                                  |

## Installation

Domino CLI can be installed via `pip` and then it can be executed as a standalone CLI tool. In order to install,
execute the following command in the terminal:

* On Windows:
    ```shell
    py -m pip install domino-cli
    # or
    pip install domino-cli
    ```
* On Linux:
    ```shell
    python3 -m pip install domino-cli
    ```

## Execution

Domino CLI can be executed from any terminal with Python. First the `DOMINO_BASE_URL` parameter must be defined.
To do this, execute the following command in the terminal:

* On Windows:
    ```shell
    set DOMINO_BASE_URL=<your_domino_instance_url>
    ```
* On Linux:
    ```shell
    export DOMINO_BASE_URL=<your_domino_instance_url>
    ```

Notes:
* With the same approach you can set the other supported environment variables as well.
* You may consider setting the environment variables permanently in the supported way of your platform. 

After this step, you can start Domino CLI:
```shell
domino-cli
```

## Usage
After successfully starting up Domino CLI you should see its prompt (`Domino CLI >`) along with some start-up messages.
Now it's time to start playing around with the commands - the supported ones are the following:

### Generic commands

```
help
```
Anytime you feel unsure how to use the tool, just type this command to have the in-application help text printed.
This will also be printed in case you type an unsupported command or hit enter without typing any commands.

```
exit
```
This command doesn't really need any explanation, it makes the tool quit.

```
auth <--encrypt-password|--generate-token|--open-session|--set-mode <direct|oauth>>
```
Authentication command serves three different purposes based on the provided flag.
* `--encrypt-password`: Provides a utility to hash the provided password with BCrypt.
    The generated hash can be used in Domino's configuration as its management access account password.
* `--generate-token`: Authenticates with Domino in order to generate a management access token.
    The generated token can be used by external systems needing access to Domino.
* `--open-session`: Authenticates with Domino in order to generate a management access token AND
    stores it in the tool's security context. Opening a session is always needed to access lifecycle commands.
    Opening a session is only needed once every time you start the tool, but the token is stored only in memory,
    so you always need to open a session after starting the tool.
* `--set-mode <direct|oauth>`: Changes the active authentication mode. Since CLI v1.3.0, it's possible to use an
    external OAuth 2.0 Authorization Server to acquire access token for Domino. Please note, that both Domino and
    Domino CLI must be registered clients on the specified authorization server; as well as Domino must be configured
    to accept the token issued by the configured authorization server. The default auth mode is the legacy one,
    called "direct". Please make sure to specify the required OAuth parameters before changing the auth mode to "oauth".
    Also, this feature is only supported in Domino v1.5.0 and above.
    
Opening a session and generating a token require full authentication, therefore the tool asks for your configured 
(on Domino side) management account username and password (only in direct auth mode). You can speed up the process by 
predefining the credentials as environment variables (see [Configuration](#configuration) section). Please be warned 
that by setting the password as an environment variable you cause a potential security vulnerability to your system. 
Keeping this in mind please handle this option with caution!

### Lifecycle-management commands

The commands below work only in case the proper application registrations have already been made in Domino.
The `app` parameter of the commands always refer to an application's registered identifier.

```
deploy <app> <latest|version>
```
Instructs Domino to deploy the specified version of the given application. The application and its selected version 
must be already uploaded to the target server via Domino. Specify the keyword `latest` to let Domino decide which 
version to be deployed, or provide an existing version number of the application.

```
start <app>
```
Instructs Domino to start the currently deployed version of the application.

```
stop <app>
```
Instructs Domino to stop the currently running instance of the application.

```
restart <app>
```
Instructs Domino to restart the currently running instance of the application.

```
info <app>
```
Instructs Domino to query the application's info endpoint and returns the results.

### Configuration wizards

Domino CLI also provides configuration wizards which help to properly create Domino configuration files.
Currently one configuration wizard is supported by the tool, but the list of wizards will be extended soon.

```
wizard deployment
```
Starts wizard that helps to create a Domino application deployment configuration. Usage notes:
* Fixed choice steps are indicated by displaying the choices with a number in square brackets at the beginning
of the line. Type the desired number and hit enter to select your choice.
* Some steps may expect multiple responses. Hit enter after each of your answers. To finalize the step hit enter
on an empty line.
* Resulted configuration can be either displayed on console or written to file. If you chose to show the result
on console, simply copy the displayed config into your existing Domino deployment config file. If you want to 
write the results to file, you need to define the file path when prompted. Having an already existing deployment
configuration file will cause the tool to merge the newly created config with the existing file.

```
wizard coordinator
```
Starts wizard that helps to create a Domino Platform Coordinator configuration.
```
wizard docker-agent
```
Starts wizard that helps to create a Domino Platform Docker Agent configuration.
```
wizard bin-exec-agent
```
Starts wizard that helps to create a Domino Platform Binary Executable Agent configuration.
```
wizard installer
```
Starts wizard that helps to install the currently available Domino Platform components (Domino Coordinator, Domino 
Docker Agent, and Domino Binary Executable Agent). The first two are installed as Docker containers, while the last
one is installed as a Systemd service. Please note, that because of this, Domino Binary Executable Agent installer 
supports Linux OS only (tested on Ubuntu).
