import unittest

from core.service.wizard.transformer.RegConfigWizardResultTransformer import RegConfigWizardResultTransformer

_REG_CONFIG_EXECUTABLE_RAW: dict = {
    "reg_name": "app1",
    "source_type": "filesystem",
    "exec_type": "executable",
    "src_home": "/home",
    "src_bin_name": "app1-exec.jar",
    "exec_user": "app_user",
    "exec_args": [
        "--arg1",
        "--arg2"
    ],
    "hc_enable": "yes",
    "hc_delay": "3 seconds",
    "hc_timeout": "2 seconds",
    "hc_max_attempts": 2,
    "hc_endpoint": "http://localhost:8099/health"
}
_REG_CONFIG_EXECUTABLE_TRANSFORMED: dict = {
    "domino": {
        "registrations": {
            "app1": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app1-exec.jar"
                },
                "execution": {
                    "via": "EXECUTABLE",
                    "as-user": "app_user",
                    "args": [
                        "--arg1",
                        "--arg2"
                    ]
                },
                "health-check": {
                    "enabled": True,
                    "delay": "3 seconds",
                    "timeout": "2 seconds",
                    "max-attempts": 2,
                    "endpoint": "http://localhost:8099/health"
                }
            }
        }
    }
}

_REG_CONFIG_RUNTIME_RAW: dict = {
    "reg_name": "app2",
    "source_type": "filesystem",
    "exec_type": "runtime",
    "src_home": "/home",
    "src_bin_name": "app2-exec.jar",
    "runtime_name": "java",
    "exec_user": "app_user",
    "exec_args": [
        "--arg1"
    ],
    "hc_enable": "no",
}
_REG_CONFIG_RUNTIME_TRANSFORMED: dict = {
    "domino": {
        "registrations": {
            "app2": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app2-exec.jar"
                },
                "execution": {
                    "via": "RUNTIME",
                    "as-user": "app_user",
                    "args": [
                        "--arg1"
                    ]
                },
                "runtime": "java",
                "health-check": {
                    "enabled": False
                }
            }
        }
    }
}

_REG_CONFIG_SERVICE_RAW: dict = {
    "reg_name": "app3",
    "source_type": "filesystem",
    "exec_type": "service",
    "src_home": "/home",
    "src_bin_name": "app3-exec.jar",
    "exec_cmd_name": "app3-svc",
    "hc_enable": "no",
}
_REG_CONFIG_SERVICE_TRANSFORMED: dict = {
    "domino": {
        "registrations": {
            "app3": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app3-exec.jar"
                },
                "execution": {
                    "via": "SERVICE",
                    "command-name": "app3-svc"
                },
                "health-check": {
                    "enabled": False
                }
            }
        }
    }
}


class RegConfigWizardResultTransformerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.reg_config_wizard_result_transformer: RegConfigWizardResultTransformer = RegConfigWizardResultTransformer()

    def test_should_transform(self):

        for (source, expected_target) in RegConfigWizardResultTransformerTest._prepare_parameters():
            with self.subTest("answer dictionary transformation", source=source, expected_target=expected_target):

                # when
                result: dict = self.reg_config_wizard_result_transformer.transform(source)

                # then
                self.assertEqual(result, expected_target)

    @staticmethod
    def _prepare_parameters():
        return [
            (_REG_CONFIG_EXECUTABLE_RAW, _REG_CONFIG_EXECUTABLE_TRANSFORMED),
            (_REG_CONFIG_RUNTIME_RAW, _REG_CONFIG_RUNTIME_TRANSFORMED),
            (_REG_CONFIG_SERVICE_RAW, _REG_CONFIG_SERVICE_TRANSFORMED)
        ]


if __name__ == "__main__":
    unittest.main()
