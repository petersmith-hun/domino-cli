# Domino CLI

Domino CLI is a command line interface tool written in Python for 
[Domino deployment orchestration application](https://github.com/petersmith-hun/domino-deployment-orchestration).
Its purpose is to provide a convenient way of controlling Domino via its REST interface.

## Requirements

* Domino CLI requires Python 3.x for execution (tested on Python 3.7 and 3.8).
* It is executable both on Windows and Linux systems.

## Configuration

The tool can be configured via the following environment variables:

| Environment variable  | Mandatory? | Description                                                                    |
|-----------------------|------------|--------------------------------------------------------------------------------|
| DOMINO_BASE_URL       | Yes        | URL of Domino instance to be controlled, e.g. http://localhost:8080/domino     |
| DOMINO_CLI_USERNAME   | No         | Optional predefined username for accessing Domino                              |
| DOMINO_CLI_PASSWORD   | No         | Optional predefined password for accessing Domino                              |
| DOMINO_CLI_DEBUG_MODE | No         | Optional debug switch. Currently its only effect is echoing the parsed command |

## Execution

Domino CLI can be executed from any terminal with Python. First the `DOMINO_BASE_URL` parameter must be defined.
To do this, execute the following command in the terminal:

* On Windows:
    ```
    set DOMINO_BASE_URL=<your_domino_instance_url>
    ```
* On Linux:
    ```
    export DOMINO_BASE_URL=<your_domino_instance_url>
    ```

Notes:
* With the same approach you can set the other supported environment variables as well.
* You may consider setting the environment variables permanently in the supported way of your platform. 

After this step, you can start Domino CLI (assuming you are standing in the tool's root directory):
```
python domino_cli.py
# or
py -3 domino_cli.py
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
auth <--encrypt-password|--generate-token|--open-session>
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
    
Opening a session and generating a token require full authentication, therefore the tool asks for your configured 
(on Domino side) management account username and password. You can speed up the process by predefining the credentials
as environment variables (see [Configuration](#configuration) section). Please be warned that by setting the password 
as an environment variable you cause a potential security vulnerability to your system. Keeping this in mind please
handle this option with caution!

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
wizard regconfig
```
Starts wizard that helps creating a Domino application registration. Usage notes:
* Fixed choice steps are indicated by displaying the choices with a number in square brackets at the beginning
of the line. Type the desired number and hit enter to select your choice.
* Some steps may expect multiple responses. Hit enter after each of your answers. To finalize the step hit enter
on an empty line.
* Resulted configuration can be either displayed on console or written to file. If you chose to show the result
on console, simply copy the displayed config into your existing Domino registration config file. If you want to 
write the results to file, you need to define the file path when prompted. Having an already existing registration
configuration file will cause the tool to merge the newly created config with the existing file.