from __future__ import annotations

from unittest import mock

from brother_ql_web import utils

from tests import TestCase


class CollectFontsTestCase(TestCase):
    def test_without_folder(self) -> None:
        dummy_fonts = {
            "DejaVu Serif": {"Book": "dummy", "Regular": "dummy2"},
            "Font": {"Style": "path"},
        }
        configuration = self.example_configuration
        with mock.patch.object(
            utils, "get_fonts", return_value=dummy_fonts
        ) as get_mock:
            fonts = utils.collect_fonts(configuration)
        get_mock.assert_called_once_with()
        self.assertEqual(dummy_fonts, fonts)

    def test_with_folder(self) -> None:
        dummy_fonts = {
            "DejaVu Serif": {"Book": "dummy", "Regular": "dummy2"},
            "Font": {"Style": "path"},
        }
        folder_fonts = {
            "Font": {"Style": "/path", "Another Style": "/path2"},
            "Symbol": {"Regular": "/path3"},
        }

        def get_fonts(directory: None | str = None) -> dict[str, dict[str, str]]:
            return folder_fonts if directory else dummy_fonts

        configuration = self.example_configuration
        configuration.server.additional_font_folder = "/another_path"
        with mock.patch.object(utils, "get_fonts", side_effect=get_fonts) as get_mock:
            fonts = utils.collect_fonts(configuration)

        get_mock.assert_has_calls(
            [mock.call(), mock.call("/another_path")], any_order=False
        )
        self.assertEqual(2, get_mock.call_count, get_mock.call_args_list)

        self.assertEqual(
            {
                "DejaVu Serif": {"Book": "dummy", "Regular": "dummy2"},
                "Font": {"Style": "/path", "Another Style": "/path2"},
                "Symbol": {"Regular": "/path3"},
            },
            fonts,
        )


class GetLabelSizesTestCase(TestCase):
    def test_get_label_sizes(self) -> None:
        sizes = utils.get_label_sizes()
        self.assertIn(("38", "38mm endless"), sizes)
        self.assertIn(("62x29", "62mm x 29mm die-cut"), sizes)


class GetBackendClassTestCase(TestCase):
    def test_unknown_backend(self) -> None:
        configuration = self.example_configuration
        configuration.printer.printer = "dummy"

        with self.assertRaisesRegex(
            utils.BackendGuessingError,
            r"^Could not guess the backend to use from the printer string descriptor$",
        ):
            utils.get_backend_class(configuration)

    def test_known_backend(self) -> None:
        from brother_ql.backends.linux_kernel import BrotherQLBackendLinuxKernel

        configuration = self.example_configuration
        backend = utils.get_backend_class(configuration)
        self.assertIs(backend, BrotherQLBackendLinuxKernel)
