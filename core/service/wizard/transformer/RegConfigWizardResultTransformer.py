import yaml

from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer


class RegConfigWizardResultTransformer(AbstractWizardResultTransformer):

    def transform(self, source: dict) -> str:

        target_dict: dict = self._define_base_dict(source)
        target_registration: dict = target_dict[source["reg_name"]]
        if source["source_type"] == "filesystem":
            RegConfigWizardResultTransformer._add_executable_based_registration_parameters(source, target_registration)
            RegConfigWizardResultTransformer._add_runtime_based_registration_parameters(source, target_registration)
            RegConfigWizardResultTransformer._add_service_based_registration_parameters(source, target_registration)
        RegConfigWizardResultTransformer._add_health_check_parameters(source, target_registration)

        return yaml.dump(target_dict)

    @staticmethod
    def _define_base_dict(source: dict) -> dict:

        return {
            source["reg_name"]: {
                "source": {
                    "type": source["source_type"]
                },
                "execution": {
                    "via": RegConfigWizardResultTransformer._safe_read(source, "exec_type")
                },
                "health-check": {
                    "enabled": RegConfigWizardResultTransformer._safe_read(source, "exec_hc_enable") == "yes"
                }
            }
        }

    @staticmethod
    def _safe_read(source: dict, key: str):
        return source[key] if key in source else None

    @staticmethod
    def _add_executable_based_registration_parameters(source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "executable":
            RegConfigWizardResultTransformer._add_fs_based_registration_common_parameters(source, target_dict)
            target_dict["execution"]["as-user"] = source["exec_user"]  # TODO assignments map, automatic fill?
            target_dict["execution"]["args"] = source["exec_args"]

    @staticmethod
    def _add_runtime_based_registration_parameters(source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "runtime":
            RegConfigWizardResultTransformer._add_fs_based_registration_common_parameters(source, target_dict)
            target_dict["execution"]["as-user"] = source["exec_user"]
            target_dict["execution"]["args"] = source["exec_args"]

    @staticmethod
    def _add_service_based_registration_parameters(source: dict, target_dict: dict) -> None:

        if source["exec_type"] == "service":
            RegConfigWizardResultTransformer._add_fs_based_registration_common_parameters(source, target_dict)
            target_dict["execution"]["command-name"] = source["exec_cmd_name"]

    @staticmethod
    def _add_fs_based_registration_common_parameters(source: dict, target_dict: dict) -> None:

        target_dict["source"]["home"] = source["src_home"]
        target_dict["source"]["resource"] = source["src_bin_name"]

    @staticmethod
    def _add_health_check_parameters(source: dict, target_dict: dict) -> None:

        if target_dict["health-check"]["enabled"]:
            target_dict["health-check"]["delay"] = source["hc_delay"]
            target_dict["health-check"]["timeout"] = source["hc_timeout"]
            target_dict["health-check"]["max-attempts"] = source["hc_max_attempts"]
            target_dict["health-check"]["endpoint"] = source["hc_endpoint"]
