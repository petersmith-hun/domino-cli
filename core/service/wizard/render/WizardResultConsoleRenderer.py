import yaml


class WizardResultConsoleRenderer:
    """
    Console based wizard result rendering.
    """
    def render(self, result: dict) -> None:
        """
        Renders a wizard's transformed (target) dictionary object as YAML structure and prints it to console.

        :param result: target dictionary to be rendered
        """
        yaml_result = yaml.dump(result, sort_keys=False)
        print("\nCopy the relevant part of the YAML document below in your Domino Platform component "
              "instance's configuration file\n")
        print("# --- Configuration starts here ---\n")
        print(yaml_result)
        print("# --- End of configuration ---")
