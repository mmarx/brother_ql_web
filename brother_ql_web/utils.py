from __future__ import annotations

import sys
from typing import cast

from brother_ql.backends import backend_factory, BrotherQLBackendGeneric, guess_backend
from brother_ql.devicedependent import label_type_specs, label_sizes
from brother_ql_web.configuration import Configuration
from brother_ql_web.font_helpers import get_fonts

if sys.version_info < (3, 9):
    from typing import Type

    BACKEND_TYPE = Type[BrotherQLBackendGeneric]
else:
    BACKEND_TYPE = type[BrotherQLBackendGeneric]


def collect_fonts(configuration: Configuration) -> dict[str, dict[str, str]]:
    fonts = get_fonts()
    if configuration.server.additional_font_folder:
        fonts.update(get_fonts(configuration.server.additional_font_folder))
    return fonts


def get_label_sizes() -> list[tuple[str, str]]:
    return [(name, cast(str, label_type_specs[name]["name"])) for name in label_sizes]


class BackendGuessingError(ValueError):
    pass


def get_backend_class(configuration: Configuration) -> BACKEND_TYPE:
    try:
        selected_backend = guess_backend(configuration.printer.printer)
    except ValueError:
        raise BackendGuessingError(
            "Could not guess the backend to use from the printer string descriptor"
        )
    return cast(
        BACKEND_TYPE,
        backend_factory(selected_backend)["backend_class"],
    )
