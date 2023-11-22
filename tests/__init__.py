from functools import cached_property
from pathlib import Path
from unittest import TestCase as _TestCase

from brother_ql_web.configuration import Configuration


class TestCase(_TestCase):
    @cached_property
    def example_configuration_path(self) -> str:
        return str(Path(__file__).parent.parent / "config.example.json")

    @property
    def example_configuration(self) -> Configuration:
        return Configuration.from_json(self.example_configuration_path)
