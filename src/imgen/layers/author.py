import logging

from typing import Tuple
from PIL import ImageDraw, ImageFont, Image as Im
from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

from result import Result, Ok, Err
from imgen.imgen_utils import ImGenUtils
from definitions import IM_MODE,COLOR_TRANSPARENT, FONT_AUTHOR_SCALE_FACTOR, FONT_SIZE


_logger = logging.getLogger(__name__)


def create( 
    text: str, 
    size: Tuple[int, int], 
    margin: int,
    walker_w: int,
    font_face: str, 
    font_color: str, 
    font_size: int = 0 ) -> Result[Image, Exception]:
    
    try:
        scaled_font_size = ImGenUtils.scale_font_size(font_size=font_size, canvas_w=size[0], factor=FONT_AUTHOR_SCALE_FACTOR)
        font_size = scaled_font_size if scaled_font_size > 0 else FONT_SIZE
        text_layer = Im.new( IM_MODE, size, COLOR_TRANSPARENT )
        font_tt: FreeTypeFont = ImageFont.truetype( font_face, font_size )
        pos: Tuple[int, int] = get_text_position( text, text_layer, font_tt, font_size, margin, walker_w )

        draw = ImageDraw.Draw( text_layer )
        draw.text( xy=pos, text=text, fill=font_color, font=font_tt, align='right')

        return Ok( text_layer )

    except Exception as err:
        _logger.error( err, exc_info=True )
        return Err(err)
        
    


def get_text_position( 
    text: str, 
    canvas: Image, 
    font: FreeTypeFont, 
    font_size: int,
    margin: int, 
    walker_w: int ) -> Tuple[int, int]:
    
    """ Gets the bottom right coords for the author name """
    try:
        txt_w, txt_h = ImageDraw.Draw( canvas ).textsize( text, font )
        canvas_w, canvas_h = canvas.size

        x = canvas_w - txt_w - font_size - walker_w - margin
        y = canvas_h - txt_h - font_size - margin

        return int(x), int(y)

    except Exception as err:
        _logger.error( err, exc_info=True )
        return 0, 0