import logging

from typing import Tuple
from PIL import Image as Im
from PIL.Image import Image

from result import Result, Ok, Err
from imgen.imgen_utils import ImGenUtils
from definitions import COLOR_TRANSPARENT, IM_MODE, IM_HEIGHT


_logger = logging.getLogger(__name__)


def create( size: Tuple[int, int], margin: int = 0, walker_asset: Image = None ) -> Result[Tuple[Image, Image], Exception] :
    """
    Gets walker asset and creates walker_layer

    :returns `Result[(walker_layer, walker_asset), Exception]`
    """
    if walker_asset is None:
        match get_walker_asset():
            case Ok( asset ): walker_asset = asset
            case Err( err ): 
                _logger.error( err, exc_info=True )
                match get_walker_placeholder():
                    case Ok( placehoder ): walker_asset = placehoder
                    case Err(err): return Err(err)

    width, height = size
    
    match gen_walker_layer( walker_asset, width = width, height = height, margin = margin ):
        case Ok( layer ): return Ok((layer, walker_asset))
        case Err( err ): return Err(err)
        


def get_walker_asset() -> Result[Image, Exception] :
    """ Loads the walker img asset. 
    Tries from local dir, if it can't will grab from url and save it to local folder"""
    filename: str = 'walker.png'

    match ImGenUtils.get_im_with_fallback(filename = filename):
        case Ok( walker ): return Ok( walker )
        case Err( err ):
            _logger.error( err, stack_info=True )
            match get_walker_placeholder():
                case Ok( walker ): return Ok(walker)
                case Err( err ): return Err( err )


def gen_walker_layer( walker_asset: Image, *, width: int, height: int, margin: int ) -> Result[Image, Exception]:

    def get_offset( base: Image, walker: Image,  margin: int = 0) -> Tuple[int, int]:
        base_w, base_h = base.size
        walker_w, walker_h = walker.size
        paste_w = base_w - walker_w - margin
        paste_h = base_h - walker_h - margin
        return ( paste_w, paste_h )

    try:
        layer: Image = Im.new( IM_MODE, (width, height), COLOR_TRANSPARENT )
        walker_asset = ImGenUtils.resize_im_by_height( origin = walker_asset, dest = layer )
        offset: Tuple[int, int] = get_offset( layer, walker_asset, margin )
        layer.paste( walker_asset, offset, walker_asset )

        return Ok(layer)

    except Exception as err:
        return Err(err)


def get_walker_placeholder() -> Result[Image, Exception]:

    try:
        size = get_walker_size()
        placeholder =Im.new( IM_MODE, size=size, color=COLOR_TRANSPARENT )
        return Ok( placeholder )

    except Exception as err:
        return Err( err )


def get_walker_size( walker: Image = None ) -> Tuple[int, int, Exception]:
    """ 
    Tries to get walker image size. It will return an aproximation of the desired walker_asset (case get_walker fails) 
    :returns `(width, height, Exception)`
    """

    try:
        w, h = walker.size
        return (w, h, None)

    except Exception as err:

        h = int(IM_HEIGHT * 0.02)
        w = int( h / 2 )

        h = h if h > 0 else 1
        w = w if w > 0 else 1

        return (w, h, err)