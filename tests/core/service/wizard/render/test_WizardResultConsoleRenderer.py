import unittest
from unittest import mock

from domino_cli.core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer


class WizardResultConsoleRendererTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_console_renderer: WizardResultConsoleRenderer = WizardResultConsoleRenderer()

    @mock.patch("builtins.print", side_effect=print)
    def test_should_render_create_yaml_document_from_dict(self, print_mock):

        # given
        source_dict: dict = {"root": {"key_b": True, "key_a": "value", "key_c": 1234}}

        # when
        self.wizard_result_console_renderer.render(source_dict)

        # then
        self.assertEqual(print_mock.call_count, 5)
        print_mock.assert_has_calls([
            mock.call("root:\n  key_b: true\n  key_a: value\n  key_c: 1234\n")
        ])


if __name__ == "__main__":
    unittest.main()
