from unittest import mock

from brother_ql_web.__main__ import main
from brother_ql_web.configuration import Font

from tests import TestCase


class Backend:
    pass


class MainTestCase(TestCase):
    def test_main(self) -> None:
        fonts = {
            "DejaVu Serif": {"Book": "dummy", "Regular": "dummy2"},
        }
        label_sizes = [("62", "62mm labels"), "42", "42mm labels"]

        with (
            mock.patch(
                "sys.argv",
                [
                    "brother_ql_web/__main__",
                    "--configuration",
                    self.example_configuration_path,
                ],
            ),
            mock.patch("logging.basicConfig") as basic_config_mock,
            mock.patch(
                "brother_ql_web.utils.collect_fonts", return_value=fonts
            ) as fonts_mock,
            mock.patch(
                "brother_ql_web.utils.get_label_sizes", return_value=label_sizes
            ) as labels_mock,
            mock.patch(
                "brother_ql_web.utils.get_backend_class", return_value=Backend
            ) as backend_mock,
            mock.patch("brother_ql_web.web.main") as main_mock,
        ):
            main()

        configuration = self.example_configuration
        configuration.label.default_font = Font(family="DejaVu Serif", style="Book")

        basic_config_mock.assert_called_once_with(level="WARNING")
        main_mock.assert_called_once_with(
            configuration=configuration,
            fonts=fonts,
            label_sizes=label_sizes,
            backend_class=Backend,
        )
        fonts_mock.assert_called_once_with(configuration)
        labels_mock.assert_called_once_with()
        backend_mock.assert_called_once_with(configuration)
