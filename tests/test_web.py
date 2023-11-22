from unittest import TestCase


class GetConfigTestCase(TestCase):
    def test_get_config(self) -> None:
        pass


class IndexTestCase(TestCase):
    def test_index(self) -> None:
        # Should redirect.
        pass


class ServeStaticTestCase(TestCase):
    def test_serve_static(self) -> None:
        # Should be correct content.
        pass


class LabeldesignerTestCase(TestCase):
    def test_labeldesigner(self) -> None:
        pass


class GetLabelParametersTestCase(TestCase):
    def test_all_set(self) -> None:
        pass

    def test_mostly_default_values(self) -> None:
        pass


class GetPreviewImageTestCase(TestCase):
    def test_base64(self) -> None:
        pass

    def test_plain_bytes(self) -> None:
        pass


class PrintTextTestCase(TestCase):
    def test_lookup_error(self) -> None:
        # TODO: Where can this error be raised?
        pass

    def test_no_text(self) -> None:
        pass

    def test_debug_mode(self) -> None:
        pass

    def test_regular_mode(self) -> None:
        pass


class MainTestCase(TestCase):
    def test_main(self) -> None:
        pass
