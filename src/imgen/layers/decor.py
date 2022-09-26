import logging

from typing import Tuple
from PIL.Image import Image

from result import Result, Ok, Err
from imgen.imgen_utils import ImGenUtils
from imgen.layers import walker
from definitions import DECOR_WALKER_FEET_PADDING_RATIO, DECOR_LINE_H_FACTOR, IM_WIDTH, IM_HEIGHT, DECOR_SIZE_MARGIN_FACTOR


_logger = logging.getLogger(__name__)


def create( 
    walker_asset: Image, 
    bkg_layer: Image, 
    margin: int,
    color: str,
    line_height: int = None ) -> Result[Image, Exception]:

    """
    Generates bottom decor layer
    :walker_asset `Image` walker asset image
    :bkg_layer `Image` background layer
    :margin `int` canvas margin in pixels
    :line_height** `int` decor (bar) height in pixels

    **Avoid passing `line_height`. If you do it will be set do (n) pixels. If you don't it will be nicelly calculated. Eg (height)600 => (line_height)2
    """
    decor_bottom: Image = None
    walker_h: int = int()
    base_w, base_h = (int(), int())

    try:
        base_w, base_h = bkg_layer.size
    except Exception as err:
        _logger.warn(err)
        base_w, base_h = (IM_WIDTH, IM_HEIGHT)


    match gen_bottom_decor( walker_asset, margin, (base_w, base_h), color, line_height ):
        case Ok( img ): decor_bottom = img
        case Err( err ): return Err( err )

    _, walker_h, size_err = walker.get_walker_size( walker_asset )

    if size_err:
        _logger.warn('ImGen.gen_decor_layer: %s',size_err)

    decor_offset_w: int = margin
    decor_offset_h: float = (base_h - margin) - ( walker_h * DECOR_WALKER_FEET_PADDING_RATIO)
    decor_offset: Tuple[int, int] = ( int(decor_offset_w), int( decor_offset_h) )

    try:
        layer = bkg_layer
        layer.paste( decor_bottom, decor_offset, decor_bottom )
        return Ok(layer)
        
    except Exception as err:
        return Err(err)


def gen_bottom_decor( 
    walker_asset: Image,
    margin: int, 
    size: Tuple[int, int],
    color: str,
    line_height: int = None ) -> Result[Image, Exception]:
    """ 
    Creates a simple line offsetting `walker_asset` width.

    Avoid passing `line_height`. If you do it will be set do (n) pixels.

    If you don't it will be nicelly calculated. Eg (height)600 => (line_height)2
    """
    walker_w: int = 1
    base_w, base_h = size

    try:
        if line_height is None or line_height == 0:
            line_height = int( base_h * DECOR_LINE_H_FACTOR )

    except Exception as line_err:
        _logger.warn('ImGen.gen_bottom_decor: %s',line_err)
        line_height = 2

    walker_w, _, size_err = walker.get_walker_size( walker_asset )

    if size_err:
        _logger.warn('ImGen.gen_bottom_decor: %s',size_err)

    decor_size_h: int = line_height
    decor_size_w = int(base_w - walker_w - ( margin * DECOR_SIZE_MARGIN_FACTOR ))

    decor_size = ( abs(decor_size_w), abs(decor_size_h) )

    return ImGenUtils.im_new( decor_size, color )