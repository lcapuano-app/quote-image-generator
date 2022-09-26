import logging
import math
import textwrap

from typing import List, Tuple
from PIL import ImageDraw, ImageFont, Image as Im
from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

from result import Result, Ok, Err
from imgen.imgen_utils import ImGenUtils
from definitions import ( 
    IM_MODE, 
    COLOR_TRANSPARENT,
    FONT_SIZE, 
    TEXT_MULTI_WRAP, 
    FONT_QUOTE_SCALE_FACTOR,
    COLOR_GOLD,
)


_logger = logging.getLogger(__name__)


def create( 
    text: str, 
    size: Tuple[int, int],
    font_face: str, 
    font_color: str, 
    wrap_width: int,
    font_size: int = 0,
    stroke_width: int = 1,
    stroke_fill: str = COLOR_GOLD
):
    
    try:
        text_layer: Image = Im.new( IM_MODE, size, COLOR_TRANSPARENT )
        adjusted_text: Tuple[str, List[str]] = adjust_quote_text( text, wrap_width )
        quote_text, wrapped = adjusted_text
        font_size = adjust_font_size(text_layer, adjusted_text, font_face, font_size, FONT_QUOTE_SCALE_FACTOR )
        font_tt: FreeTypeFont = ImageFont.truetype( font_face, font_size )
        pos: Tuple[int, int] = get_quote_text_pos( quote_text, text_layer, font_tt )
        

        draw = ImageDraw.Draw( text_layer )
        draw.text( 
            xy = pos, 
            text = quote_text, 
            fill = font_color, 
            font=font_tt, 
            anchor = 'ms', 
            align = 'center', 
            stroke_width = stroke_width, 
            stroke_fill=  stroke_fill
        )

        return Ok( text_layer )

    except Exception as err:
        _logger.error( err, exc_info=True )
        return Err(err)


def adjust_quote_text( text: str, wrap_width: int = TEXT_MULTI_WRAP ) -> Tuple[ str, List[str] ]:

    try:
        text = '“' + text + '”'
        wrapped: List[str] = textwrap.wrap( text, wrap_width )
        text = '\n'.join( wrapped )

        return text, wrapped
    
    except Exception as err:
        _logger.error(err, exc_info=True)
        return text, [ text ]


def get_quote_text_pos( text: str, canvas: Image, font_tt: FreeTypeFont ) -> Tuple[int, int]:
    try:
        _, txt_h = ImageDraw.Draw( canvas ).textsize( text, font_tt )
        canvas_w, canvas_h = canvas.size

        x = canvas_w // 2
        y =   (canvas_h - txt_h) // 2

        return x,y

    except Exception as err:
        _logger.error(err, exc_info=True)
        return 0, 0


def adjust_font_size( 
    canvas: Image, 
    adjusted_text: Tuple[ str, List[str] ], 
    font_face: str, 
    font_size: int, 
    scale_factor: float ) -> int:

    """ Gets the biggest possible value, but still nice,  to font size. """
    try:
        canvas_w, _ = canvas.size
        text, wrapped = adjusted_text

        scaled_size: int = ImGenUtils.scale_font_size( font_size=font_size, canvas_w=canvas_w, factor=scale_factor )

        font_size = scaled_size if scaled_size > 0 else FONT_SIZE
        font_tt: FreeTypeFont = ImageFont.truetype( font_face, font_size )

        txt_w, _ = ImageDraw.Draw( canvas ).textsize(text, font_tt )

        txt_img_limit = canvas_w - (canvas_w // 5)
        safe_font_size = font_size

        if len(wrapped) > 1:
            txt_img_limit = canvas_w - (canvas_w // 7)

        while txt_w < txt_img_limit:
            font_tt = ImageFont.truetype( font_face, int(font_size) )
            txt_w, _ = ImageDraw.Draw( canvas ).textsize( text, font_tt )

            if txt_w < txt_img_limit:
                safe_font_size = font_size

            font_size *= 1.1

        return math.ceil(safe_font_size)

    except Exception as err:
        _logger.error(err, exc_info=True)
        return font_size

