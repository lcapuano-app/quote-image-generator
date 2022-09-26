import logging

from typing import Tuple
from PIL import ImageOps
from PIL.Image import Image

from result import Result, Ok, Err
from imgen.imgen_utils import ImGenUtils
from definitions import ( 
    FALLBACK_DIR, 
    COLOR_BG, IM_HEIGHT, 
    IM_WIDTH,
    ASSETS_DIR
)


_logger = logging.getLogger(__name__)


def create( 
    size: Tuple[int, int], 
    color: str, 
    img_name: str, 
    resize_factor: float, 
    rotate_deg: float, 
    img_alpha: int ) -> Result[Image, Exception]:
    """
    Generates quote's img background 
    :size `tuple [width, height]`
    :color `"rgba(r,g,b,a)"`
    :img_name `str` author's image name (url and local)
    :resize_factor `float` how much the author's image will grow or shrink
    :rotate_deg `float` how much the author's image will rotate
    :img_alpha `int` author's pic alpha. Lower numbers = darken image
    """

    bkg_layer: Image = None
    author_layer: Image = None
    
    match gen_layer( size, color ):
        case Ok( bkg ): bkg_layer = bkg 
        case Err( err ): 
            _logger.error(err, exc_info=True, )
            return Err(err)

    match gen_author_layer( bkg_layer, img_name, resize_factor, rotate_deg, img_alpha ):
        case Ok( layer ): author_layer = layer
        case Err( err ):
            _logger.error(err, exc_info=True)
            author_layer = bkg_layer

    try:
        bkg_layer.paste( author_layer, (0, 0), author_layer )
        return Ok( bkg_layer )

    except Exception as err:
        _logger.error(err, exc_info=True, )
        return Err(err)


def gen_layer( size: Tuple[int, int], color: str ) -> Result[Image, Exception]:
    """
    Generates quote's background layer
    :size `tuple [width, height]`
    :color `"rgba(r,g,b,a)"`
    """
               
    try:
        width, height = size
        height = abs(int( height ))
        width = abs(int( width ))
        size = ( width, height )
        if color is not None:
            color = color.lower() if color.lower().startswith('rgb') else COLOR_BG
    
    except Exception as err:
        _logger.warn( err )
        color = COLOR_BG
        size = (IM_WIDTH, IM_HEIGHT)
     

    match ImGenUtils.im_new( size, color ):
        case Ok( bkg ): return Ok( bkg )
        case Err( err ):
            _logger.error(err)
            match ImGenUtils.get_im_with_fallback( filename='bkg.png', dirname=FALLBACK_DIR ):
                case Ok( im_bkg ): return Ok( im_bkg )
                case Err( err ):
                    return Err(err)


def gen_author_layer( 
    bkg_layer: Image, img_name: str, resize_factor: float, rotate_deg: float, img_alpha: int ) -> Result[Image, Exception]:

    """
    Creates author layer (B&W author pic with scale and rotate) to be further pasted into background.
    :bkg_layer `Image` background layer
    :img_name `str` author's image name (url and local)
    :resize_factor `float` how much the author's image will grow or shrink
    :rotate_deg `float` how much the author's image will rotate
    :img_alpha `int` author's pic alpha. Lower numbers = darken image
    """
   
    author_asset: Image = None

    im_with_fallback = ImGenUtils.get_im_with_fallback( filename=img_name, dirname=ASSETS_DIR )
    match im_with_fallback:
        case Ok( asset ): author_asset = asset
        case Err( err ): 
            _logger.error( err, exc_info=True)
            return Err(err)

    resize_over = ImGenUtils.resize_over_bkg_size( bkg=bkg_layer, origin=author_asset, factor=resize_factor )
    match resize_over:
        case Ok( resized ): author_asset = resized
        case Err( err ): 
            _logger.error( err, exc_info=True)
            return Err(err)

    try:
        author_asset = ImageOps.grayscale( author_asset )
        author_asset = author_asset.rotate( angle=rotate_deg )
        author_asset = crop_author_asset( bkg=bkg_layer, asset=author_asset )
        author_asset.putalpha( img_alpha )

        return Ok( author_asset )
    
    except Exception as err:
        _logger.error( err, exc_info=True)
        return Err(err)


def crop_author_asset( *, bkg: Image, asset: Image ) -> Image:

    try:
        asset_w, asset_h = asset.size
        bkg_w, bkg_h = bkg.size

        crop_w = (asset_w - bkg_w) // 2
        crop_h = (asset_h - bkg_h) // 2
        crop_border = ( crop_w, crop_h, crop_w, crop_h ) #(left, top, right, bottom)

        asset = ImageOps.crop( image=asset, border=crop_border )
        
        return asset

    except Exception as err:
        raise err

