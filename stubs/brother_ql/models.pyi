from __future__ import annotations

from _typeshed import Incomplete
from typing import NoReturn
from brother_ql.helpers import ElementsManager as ElementsManager

class Model:
    identifier: str
    min_max_length_dots: tuple[int, int]
    min_max_feed: tuple[int, int]
    number_bytes_per_row: int
    additional_offset_r: int
    mode_setting: bool
    cutting: bool
    expanded_mode: bool
    compression: bool
    two_color: bool
    @property
    def name(self) -> str: ...
    def __init__(
        self,
        identifier: str,
        min_max_length_dots: tuple[int, int],
        min_max_feed: tuple[int, int] = (35, 1500),
        number_bytes_per_row: int = 90,
        additional_offset_r: int = 0,
        mode_setting: bool = True,
        cutting: bool = True,
        expanded_mode: bool = True,
        compression: bool = True,
        two_color: bool = False,
    ) -> NoReturn: ...
    def __lt__(self, other: Model) -> bool: ...
    def __le__(self, other: Model) -> bool: ...
    def __gt__(self, other: Model) -> bool: ...
    def __ge__(self, other: Model) -> bool: ...

ALL_MODELS: list[Model]

class ModelsManager(ElementsManager):
    DEFAULT_ELEMENTS: list[Model]
    ELEMENTS_NAME: str
