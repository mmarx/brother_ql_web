from _typeshed import Incomplete
from brother_ql import BrotherQLUnsupportedCmd as BrotherQLUnsupportedCmd
from brother_ql.devicedependent import (
    DIE_CUT_LABEL as DIE_CUT_LABEL,
    ENDLESS_LABEL as ENDLESS_LABEL,
    PTOUCH_ENDLESS_LABEL as PTOUCH_ENDLESS_LABEL,
    ROUND_DIE_CUT_LABEL as ROUND_DIE_CUT_LABEL,
    label_type_specs as label_type_specs,
    right_margin_addition as right_margin_addition,
)
from brother_ql.image_trafos import filtered_hsv as filtered_hsv
from brother_ql.raster import BrotherQLRaster as BrotherQLRaster
from PIL import Image

logger: Incomplete

def convert(
    qlr: BrotherQLRaster,
    images: list[str | Image.Image],
    label: str,
    **kwargs: bool | int | str,
) -> bytes: ...
