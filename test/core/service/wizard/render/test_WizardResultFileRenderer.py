import unittest
from unittest import mock
from unittest.mock import mock_open

from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer


class WizardResultFileRendererTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_file_renderer: WizardResultFileRenderer = WizardResultFileRenderer()

    @mock.patch("builtins.input", return_value="result.yml")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("yaml.dump")
    def test_should_render_create_yaml_document_from_dict_without_merge(self, yaml_mock, open_mock, input_mock):

        # given
        source_dict: dict = {"root": {"key_b": True, "key_a": "value", "key_c": 1234}}

        # when
        self.wizard_result_file_renderer.render(source_dict)

        # then
        input_mock.assert_called_once_with("File path > ")
        open_mock.assert_called_once_with("result.yml", "w")
        yaml_mock.assert_called_once_with(source_dict, open_mock(), sort_keys=False)

    @mock.patch("builtins.input", return_value="result.yml")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("yaml.dump")
    @mock.patch("yaml.load")
    @mock.patch("os.path.exists", return_value=True)
    def test_should_render_create_yaml_document_from_dict_with_merge(self, path_exists_mock, yaml_load_mock, yaml_dump_mock, open_mock, input_mock):

        # given
        source_dict: dict = {"root": {"key_b": True, "key_a": "value", "key_c": 1234}}
        existing_dict: dict = {"root": {"key_existing": "abcd"}}
        expected_dict = {"root": {"key_existing": "abcd", "key_b": True, "key_a": "value", "key_c": 1234}}
        yaml_load_mock.return_value = existing_dict

        # when
        self.wizard_result_file_renderer.render(source_dict, lambda context: context["root"])

        # then
        input_mock.assert_called_once_with("File path > ")
        open_mock.assert_any_call("result.yml", "r")
        open_mock.assert_any_call("result.yml", "w")
        yaml_dump_mock.assert_called_once_with(expected_dict, open_mock(), sort_keys=False)


if __name__ == "__main__":
    unittest.main()
