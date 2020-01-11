import yaml


class WizardResultConsoleRenderer:

    def render(self, result: dict):

        yaml_result = yaml.dump(result, sort_keys=False)
        print("\nCopy the relevant part of the YAML document below under domino.registrations "
              "section in your Domino instance's registrations configuration file\n")
        print("# --- Registration config starts here ---\n")
        print(yaml_result)
        print("# --- End of registration config ---")
