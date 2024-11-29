from __future__ import annotations

import logging
from dataclasses import dataclass
from io import BytesIO
from typing import cast, Literal

from brother_ql import BrotherQLRaster
from brother_ql.conversion import convert
from brother_ql.labels import ALL_LABELS, FormFactor, Label
from brother_ql_web.configuration import Configuration
from brother_ql_web import utils
from PIL import Image, ImageDraw, ImageFont
from tempfile import TemporaryDirectory
from barcode.codex import Code128
from barcode.writer import ImageWriter
from pylibdmtx import pylibdmtx

logger = logging.getLogger(__name__)
del logging


TEXT_ANCHOR = "lt"


@dataclass
class LabelParameters:
    configuration: Configuration

    font_family: str | None = None
    font_style: str | None = None
    text: str = ""
    image: bytes | None = None
    pdf: bytes | None = None
    font_size: int = 100
    label_size: str = "62"
    margin: int = 10
    threshold: int = 70
    align: str = "center"
    orientation: str = "standard"
    margin_top: int = 24
    margin_bottom: int = 45
    margin_left: int = 35
    margin_right: int = 35
    label_count: int = 1
    # TODO: Not yet taken into account. The number of dots in each direction has to be
    #       doubled. The generator/calculation methods have to be updated accordingly.
    high_quality: bool = False
    grocycode: str | None = None
    product: str | None = None
    battery: str | None = None
    chore: str | None = None
    duedate: str | None = None
    duedate_font_size: int = 60
    code_128: bool = False
    always_below_code: bool = False

    @property
    def _label(self) -> Label:
        for label in ALL_LABELS:
            if label.identifier == self.label_size:
                return label
        raise LookupError("Unknown label_size")

    @property
    def kind(self) -> FormFactor:
        return self._label.form_factor

    def _scale_margin(self, margin: int) -> int:
        return int(self.font_size * margin / 100.0)

    @property
    def margin_top_scaled(self) -> int:
        return self._scale_margin(self.margin_top)

    @property
    def margin_bottom_scaled(self) -> int:
        return self._scale_margin(self.margin_bottom)

    @property
    def margin_left_scaled(self) -> int:
        return self._scale_margin(self.margin_left)

    @property
    def margin_right_scaled(self) -> int:
        return self._scale_margin(self.margin_right)

    @property
    def fill_color(self) -> tuple[int, int, int]:
        return (255, 0, 0) if "red" in self.label_size else (0, 0, 0)

    @property
    def font_path(self) -> str:
        try:
            if self.font_family is None or self.font_style is None:
                assert self.configuration.label.default_font is not None
                self.font_family = self.configuration.label.default_font.family
                self.font_style = self.configuration.label.default_font.style
            fonts = utils.collect_fonts(self.configuration)
            path = fonts[self.font_family][self.font_style]
        except KeyError:
            raise LookupError("Couldn't find the font & style")
        return path

    @property
    def width_height(self) -> tuple[int, int]:
        width, height = self._label.dots_printable

        if height > width:
            width, height = height, width
        if self.orientation == "rotated":
            height, width = width, height
        return width, height

    @property
    def width(self) -> int:
        return self.width_height[0]

    @property
    def height(self) -> int:
        return self.width_height[1]


class GrocyCode:
    text_font_size: int
    duedate_font_size: int
    font_path: str
    code_height: int
    text: str
    duedate: str | None
    grocycode: str
    code_128: bool = False
    margin_top: int
    margin_left: int
    margin_right: int
    margin_bottom: int
    tape_width: int

    def __init__(self, parameters: LabelParameters) -> None:
        if parameters.product:
            self.text = parameters.product
        elif parameters.chore:
            self.text = parameters.chore
        elif parameters.battery:
            self.text = parameters.battery
        else:
            raise ValueError("one of product, chore, or battery must be given")

        if parameters.orientation == "rotated":
            self.tape_width = parameters.height
        else:
            self.tape_width = parameters.width

        self.duedate = parameters.duedate
        self.grocycode = parameters.grocycode or ""
        self.font_path = parameters.font_path
        self.code_128 = parameters.code_128
        self.text_font_size = parameters.font_size
        self.duedate_font_size = parameters.duedate_font_size
        self.margin_top = parameters.margin_top
        self.margin_left = parameters.margin_left
        self.margin_right = parameters.margin_right
        self.margin_bottom = parameters.margin_bottom
        self.always_below_code = parameters.always_below_code

    def text_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.font_path, self.text_font_size)

    def duedate_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.font_path, self.duedate_font_size)

    def barcode(self) -> Image.Image:
        barcode = Code128(self.grocycode, writer=ImageWriter())
        return cast(Image.Image, barcode.render())

    def datamatrix(self) -> Image.Image:
        encoded = pylibdmtx.encode(self.grocycode.encode("utf-8"), size="SquareAuto")
        return Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)

    def text_bbox(self, anchor: Tuple[int, int] = (0, 0)) -> Tuple[int, int, int, int]:
        image = Image.new("RGB", (0, 0))
        draw = ImageDraw.Draw(image)

        return draw.textbbox(anchor, self.text, self.text_font(), TEXT_ANCHOR)

    def duedate_bbox(
        self, anchor: Tuple[int, int] = (0, 0)
    ) -> Tuple[int, int, int, int]:
        if self.duedate is None:
            return (*anchor, *anchor)

        image = Image.new("RGB", (0, 0))
        draw = ImageDraw.Draw(image)

        return draw.textbbox(anchor, self.duedate, self.duedate_font(), TEXT_ANCHOR)

    def grocycode_image(self) -> Image.Image:
        code = self.barcode() if self.code_128 else self.datamatrix()
        code_bbox = (
            self.margin_left,
            self.margin_top,
            self.margin_left + code.width,
            self.margin_top + code.height,
        )

        text_below = self.always_below_code or self.code_128

        if text_below:
            text_anchor = (self.margin_left, code_bbox[3] + self.margin_top)
        else:
            text_anchor = (code_bbox[2] + self.margin_left, self.margin_top)

        text_bbox = self.text_bbox(text_anchor)
        duedate_anchor = (
            self.margin_left,
            max(code_bbox[3], text_bbox[3]) + self.margin_top,
        )
        duedate_bbox = self.duedate_bbox(duedate_anchor)

        size = (
            max(code_bbox[2], text_bbox[2], duedate_bbox[2]) + self.margin_right,
            max(code_bbox[3], text_bbox[3], duedate_bbox[3]) + self.margin_bottom,
        )

        if min(*size) > self.tape_width:
            logger.warn(
                f"code dimensions {size} too large for label with width {self.tape_width}"
            )

        if size[0] <= self.tape_width:
            rotated = False
            size = (max(size[0], self.tape_width), size[1])
        else:
            rotated = True
            size = (size[0], max(size[1], self.tape_width))

        image = Image.new("RGB", size, "white")
        draw = ImageDraw.Draw(image)

        image.paste(code, code_bbox)
        draw.text(text_anchor, self.text, "black", self.text_font(), TEXT_ANCHOR)
        if self.duedate is not None:
            draw.text(
                duedate_anchor, self.duedate, "black", self.duedate_font(), TEXT_ANCHOR
            )

        if rotated:
            image.transpose(Image.ROTATE_270)

        return (image, rotated)


def _determine_image_dimensions(
    text: str, image_font: ImageFont.FreeTypeFont, parameters: LabelParameters
) -> tuple[int, int, int, int]:
    image = Image.new("L", (20, 20), "white")
    draw = ImageDraw.Draw(image)

    left, top, right, bottom = draw.multiline_textbbox(
        xy=(0, 0), text=text, font=image_font
    )
    text_width, text_height = (right - left, bottom - top)
    width, height = parameters.width_height
    if parameters.orientation == "standard":
        if parameters.kind in (FormFactor.ENDLESS,):
            height = (
                text_height
                + parameters.margin_top_scaled
                + parameters.margin_bottom_scaled
            )
    elif parameters.orientation == "rotated":
        if parameters.kind in (FormFactor.ENDLESS,):
            width = (
                text_width
                + parameters.margin_left_scaled
                + parameters.margin_right_scaled
            )
    return width, height, text_width, text_height


def _determine_text_offsets(
    height: int,
    width: int,
    text_height: int,
    text_width: int,
    parameters: LabelParameters,
) -> tuple[int, int]:
    if parameters.orientation == "standard":
        if parameters.kind in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
            vertical_offset = (height - text_height) // 2
            vertical_offset += (
                parameters.margin_top_scaled - parameters.margin_bottom_scaled
            ) // 2
        else:
            vertical_offset = parameters.margin_top_scaled
        horizontal_offset = max((width - text_width) // 2, 0)
    elif parameters.orientation == "rotated":
        vertical_offset = (height - text_height) // 2
        vertical_offset += (
            parameters.margin_top_scaled - parameters.margin_bottom_scaled
        ) // 2
        if parameters.kind in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
            horizontal_offset = max((width - text_width) // 2, 0)
        else:
            horizontal_offset = parameters.margin_left_scaled
    return horizontal_offset, vertical_offset


def create_label_image(parameters: LabelParameters) -> Image.Image:
    if parameters.image:
        return Image.open(BytesIO(parameters.image))

    image_font = ImageFont.truetype(parameters.font_path, parameters.font_size)

    # Workaround for a bug in multiline_textsize()
    # when there are empty lines in the text:
    lines = []
    for line in parameters.text.split("\n"):
        if line == "":
            line = " "
        lines.append(line)
    text = "\n".join(lines)

    width, height, text_width, text_height = _determine_image_dimensions(
        text=text, image_font=image_font, parameters=parameters
    )
    offset = _determine_text_offsets(
        width=width,
        height=height,
        text_width=text_width,
        text_height=text_height,
        parameters=parameters,
    )

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    align = cast(Literal["left", "center", "right"], parameters.align)
    draw.multiline_text(
        offset, text, parameters.fill_color, font=image_font, align=align
    )
    return image


def image_to_png_bytes(image: Image.Image) -> bytes:
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer.read()


def generate_label(
    parameters: LabelParameters,
    configuration: Configuration,
    save_image_to: str | None = None,
    grocy: bool = False,
) -> BrotherQLRaster:
    if grocy:
        image, rotated = GrocyCode(parameters).grocycode_image()
    else:
        image = create_label_image(parameters)

    if save_image_to:
        image.save(save_image_to)

    red: bool = "red" in parameters.label_size
    rotate: int | str = 0
    if parameters.kind == FormFactor.ENDLESS:
        rotate = 0 if parameters.orientation == "standard" else 90
        if grocy and rotated:
            rotate = 90
    elif parameters.kind in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
        rotate = "auto"

    if parameters.high_quality:
        logger.warning("High quality mode is not implemented for now.")

    qlr = BrotherQLRaster(configuration.printer.model)
    convert(
        qlr,
        [image],
        parameters.label_size,
        red=red,
        threshold=parameters.threshold,
        cut=True,
        rotate=rotate,
        dpi_600=False,
    )

    return qlr


def print_label(
    parameters: LabelParameters,
    qlr: BrotherQLRaster,
    configuration: Configuration,
    backend_class: type,
) -> None:
    backend = backend_class(configuration.printer.printer)
    for i in range(parameters.label_count):
        logger.info("Printing label %d of %d ...", i + 1, parameters.label_count)
        backend.write(qlr.data)
    backend.dispose()
    del backend
