from typing import Tuple
from PIL import Image
from PIL.Image import Image as ImageType
from config import CFG
from error_log import ErrLog

class BottomDecorHandler():

  def get_decor_layer( size: Tuple[ int, int], walker: Image, color: str, margin: int = 0, height: int = 2 ) -> ImageType:
    handler = BottomDecorHandler
    layer = Image.new( mode='RGBA', size=size, color='rgba(0,0,0,0)' )
    decor = handler.__create_decor( base_image=layer, walker=walker, margin=margin, color=color, height=height )
    layer = handler.__add_bottom_decor( base_image=layer, walker=walker, decor=decor, margin=margin )
    return layer

  def __create_decor( base_image: Image, walker: Image, margin: int, color: str, height: int = 2 ) -> ImageType:
    base_w, base_h = base_image.size
    walker_w, walker_h = walker.size

    decor_size_h = height
    decor_size_w = base_w - walker_w - ( margin * 3 )

    decor_size = ( decor_size_w, decor_size_h )
    decor = Image.new( mode='RGBA', size=decor_size, color=color )

    return decor

  def __add_bottom_decor( base_image: Image, walker: Image, decor: Image, margin: int ) -> ImageType:
    base_w, base_h = base_image.size
    walker_w, walker_h = walker.size

    walker_h_ratio = CFG.WALKER_FEET_RATIO
    decor_offset_w = margin
    decor_offset_h = (base_h - margin) - ( walker_h * walker_h_ratio)

    decor_offset = ( int(decor_offset_w), int( decor_offset_h) )

    try:
      base_image.paste( decor, decor_offset, decor )
      return base_image

    except Exception as err:
      ErrLog.log( err )
      return base_image
