from _typeshed import Incomplete
from brother_ql.conversion import convert as convert
from brother_ql.devicedependent import label_type_specs as label_type_specs
from brother_ql.raster import BrotherQLRaster as BrotherQLRaster
from PIL import Image

stdout: Incomplete
logger: Incomplete

def main() -> None: ...
def create_label(
    qlr: BrotherQLRaster,
    image: str | Image.Image,
    label_size: str,
    threshold: int = ...,
    cut: bool = ...,
    dither: bool = ...,
    compress: bool = ...,
    red: bool = ...,
    **kwargs: bool | int | str,
) -> None: ...
