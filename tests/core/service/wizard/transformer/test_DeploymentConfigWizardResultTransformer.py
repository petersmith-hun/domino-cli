import unittest

from domino_cli.core.service.wizard.transformer.DeploymentConfigWizardResultTransformer import DeploymentConfigWizardResultTransformer

_DEPLOYMENT_CONFIG_EXECUTABLE_RAW: dict = {
    "deployment_name": "app1",
    "target_hosts": [
        "devlocal",
        "localhost"
    ],
    "multi_instance_enable": "no",
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
    "hc_max_attempts": "2",
    "hc_endpoint": "http://localhost:8099/health",
    "info_enable": "no"
}
_DEPLOYMENT_CONFIG_EXECUTABLE_TRANSFORMED: dict = {
    "domino": {
        "deployments": {
            "app1": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app1-exec.jar"
                },
                "target": {
                    "hosts": [
                        "devlocal",
                        "localhost"
                    ],
                    "multi-instance": {
                        "enabled": False
                    }
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
                },
                "info": {
                    "enabled": False
                }
            }
        }
    }
}

_DEPLOYMENT_CONFIG_RUNTIME_RAW: dict = {
    "deployment_name": "app2",
    "target_hosts": [
        "localhost"
    ],
    "multi_instance_enable": "no",
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
    "info_enable": "yes",
    "info_endpoint": "http://localhost:9000/actuator/info",
    "info_field_mapping": {
        "name": "$.app.name",
        "version": "$.build.version"
    }
}
_DEPLOYMENT_CONFIG_RUNTIME_TRANSFORMED: dict = {
    "domino": {
        "deployments": {
            "app2": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app2-exec.jar"
                },
                "target": {
                    "hosts": [
                        "localhost"
                    ],
                    "multi-instance": {
                        "enabled": False
                    }
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
                },
                "info": {
                    "enabled": True,
                    "endpoint": "http://localhost:9000/actuator/info",
                    "field-mapping": {
                        "name": "$.app.name",
                        "version": "$.build.version"
                    }
                }
            }
        }
    }
}

_DEPLOYMENT_CONFIG_SERVICE_RAW: dict = {
    "deployment_name": "app3",
    "target_hosts": [
        "localhost"
    ],
    "multi_instance_enable": "no",
    "source_type": "filesystem",
    "exec_type": "service",
    "src_home": "/home",
    "src_bin_name": "app3-exec.jar",
    "exec_cmd_name": "app3-svc",
    "exec_user": "app3-user",
    "hc_enable": "no",
    "info_enable": "no"
}
_DEPLOYMENT_CONFIG_SERVICE_TRANSFORMED: dict = {
    "domino": {
        "deployments": {
            "app3": {
                "source": {
                    "type": "FILESYSTEM",
                    "home": "/home",
                    "resource": "app3-exec.jar"
                },
                "target": {
                    "hosts": [
                        "localhost"
                    ],
                    "multi-instance": {
                        "enabled": False
                    }
                },
                "execution": {
                    "via": "SERVICE",
                    "as-user": "app3-user",
                    "command-name": "app3-svc"
                },
                "health-check": {
                    "enabled": False
                },
                "info": {
                    "enabled": False
                }
            }
        }
    }
}

_DEPLOYMENT_CONFIG_DOCKER_STANDARD_RAW: dict = {
    "deployment_name": "app4",
    "target_hosts": [
        "localhost"
    ],
    "multi_instance_enable": "yes",
    "instance_count": "2",
    "spread_mode": "replicate",
    "naming_strategy": "incremental-suffix",
    "port_offset": "+100",
    "source_type": "docker",
    "exec_type": "standard",
    "src_home": "http://localhost:5000/apps",
    "src_bin_name": "img_app4",
    "exec_cmd_name": "container_app4",
    "exec_args_docker_ports": {
        "9000": "9000/tcp",
        "8080": "8080"
    },
    "exec_args_docker_env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2",
        "ENV_VAR3": "value3"
    },
    "exec_args_docker_volumes": {
        "/tmp1": "/tmp1",
        "/tmp2/something": "/app/tmp:rw",
        "/tmp3/tmp": "/app/something:ro"
    },
    "exec_args_docker_network": "host",
    "exec_args_docker_restart": "unless-stopped",
    "exec_args_docker_cmd": [
        "--param1",
        "--param2"
    ],
    "hc_enable": "no",
    "info_enable": "no"
}
_DEPLOYMENT_CONFIG_DOCKER_STANDARD_TRANSFORMED: dict = {
    "domino": {
        "deployments": {
            "app4": {
                "source": {
                    "type": "DOCKER",
                    "home": "http://localhost:5000/apps",
                    "resource": "img_app4"
                },
                "target": {
                    "hosts": [
                        "localhost"
                    ],
                    "multi-instance": {
                        "enabled": True,
                        "instance-count": 2,
                        "spread-mode": "replicate",
                        "naming-strategy": "incremental-suffix",
                        "defined-names": None,
                        "port-offset": 100,
                        "host-network-base-port": None
                    }
                },
                "execution": {
                    "via": "STANDARD",
                    "command-name": "container_app4",
                    "args": {
                        "ports": {
                            "9000": "9000/tcp",
                            "8080": "8080"
                        },
                        "environment": {
                            "ENV_VAR1": "value1",
                            "ENV_VAR2": "value2",
                            "ENV_VAR3": "value3"
                        },
                        "volumes": {
                            "/tmp1": "/tmp1",
                            "/tmp2/something": "/app/tmp:rw",
                            "/tmp3/tmp": "/app/something:ro"
                        },
                        "network-mode": "host",
                        "restart-policy": "unless-stopped",
                        "command-args": [
                            "--param1",
                            "--param2"
                        ]
                    }
                },
                "health-check": {
                    "enabled": False
                },
                "info": {
                    "enabled": False
                }
            }
        }
    }
}

_DEPLOYMENT_CONFIG_DOCKER_STANDARD_RAW_2: dict = {
    "deployment_name": "app4",
    "target_hosts": [
        "localhost",
        "host2",
        "host3"
    ],
    "multi_instance_enable": "yes",
    "instance_count": "3",
    "spread_mode": "one-per-host",
    "naming_strategy": "custom-predefined",
    "defined_names": [
        "primary",
        "secondary",
        "standby"
    ],
    "port_offset": "-200",
    "host_network_base_port": "8200",
    "source_type": "docker",
    "exec_type": "standard",
    "src_home": "http://localhost:5000/apps",
    "src_bin_name": "img_app4",
    "exec_cmd_name": "container_app4",
    "exec_args_docker_ports": {
        "9000": "9000/tcp",
        "8080": "8080"
    },
    "exec_args_docker_env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2",
        "ENV_VAR3": "value3"
    },
    "exec_args_docker_volumes": {
        "/tmp1": "/tmp1",
        "/tmp2/something": "/app/tmp:rw",
        "/tmp3/tmp": "/app/something:ro"
    },
    "exec_args_docker_network": "host",
    "exec_args_docker_restart": "unless-stopped",
    "exec_args_docker_cmd": [
        "--param1",
        "--param2"
    ],
    "hc_enable": "no",
    "info_enable": "no"
}
_DEPLOYMENT_CONFIG_DOCKER_STANDARD_TRANSFORMED_2: dict = {
    "domino": {
        "deployments": {
            "app4": {
                "source": {
                    "type": "DOCKER",
                    "home": "http://localhost:5000/apps",
                    "resource": "img_app4"
                },
                "target": {
                    "hosts": [
                        "localhost",
                        "host2",
                        "host3"
                    ],
                    "multi-instance": {
                        "enabled": True,
                        "instance-count": 3,
                        "spread-mode": "one-per-host",
                        "naming-strategy": "custom-predefined",
                        "defined-names": [
                            "primary",
                            "secondary",
                            "standby"
                        ],
                        "port-offset": -200,
                        "host-network-base-port": 8200
                    }
                },
                "execution": {
                    "via": "STANDARD",
                    "command-name": "container_app4",
                    "args": {
                        "ports": {
                            "9000": "9000/tcp",
                            "8080": "8080"
                        },
                        "environment": {
                            "ENV_VAR1": "value1",
                            "ENV_VAR2": "value2",
                            "ENV_VAR3": "value3"
                        },
                        "volumes": {
                            "/tmp1": "/tmp1",
                            "/tmp2/something": "/app/tmp:rw",
                            "/tmp3/tmp": "/app/something:ro"
                        },
                        "network-mode": "host",
                        "restart-policy": "unless-stopped",
                        "command-args": [
                            "--param1",
                            "--param2"
                        ]
                    }
                },
                "health-check": {
                    "enabled": False
                },
                "info": {
                    "enabled": False
                }
            }
        }
    }
}

class DeploymentConfigWizardResultTransformerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.deployment_config_wizard_result_transformer: DeploymentConfigWizardResultTransformer = DeploymentConfigWizardResultTransformer()

    def test_should_transform(self):

        for (source, expected_target) in DeploymentConfigWizardResultTransformerTest._prepare_parameters():
            with self.subTest("answer dictionary transformation", source=source, expected_target=expected_target):

                # when
                result: dict = self.deployment_config_wizard_result_transformer.transform(source)

                # then
                self.assertEqual(result, expected_target)

    @staticmethod
    def _prepare_parameters():
        return [
            (_DEPLOYMENT_CONFIG_EXECUTABLE_RAW, _DEPLOYMENT_CONFIG_EXECUTABLE_TRANSFORMED),
            (_DEPLOYMENT_CONFIG_RUNTIME_RAW, _DEPLOYMENT_CONFIG_RUNTIME_TRANSFORMED),
            (_DEPLOYMENT_CONFIG_SERVICE_RAW, _DEPLOYMENT_CONFIG_SERVICE_TRANSFORMED),
            (_DEPLOYMENT_CONFIG_DOCKER_STANDARD_RAW, _DEPLOYMENT_CONFIG_DOCKER_STANDARD_TRANSFORMED),
            (_DEPLOYMENT_CONFIG_DOCKER_STANDARD_RAW_2, _DEPLOYMENT_CONFIG_DOCKER_STANDARD_TRANSFORMED_2)
        ]


if __name__ == "__main__":
    unittest.main()
