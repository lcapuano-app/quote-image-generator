import urllib.request
from typing import Tuple
from PIL import Image
from PIL.Image import Image as ImageType
from ..img_utils import img_resize
from config import CFG
from error_log import ErrLog

class WalkerHandler():

  def get_walker_layer( walker_asset: ImageType, size: Tuple[ int, int], margin: int = 0 ) -> ImageType:
    layer = Image.new( mode='RGBA', size=size, color='rgba(0,0,0,0)' )
    layer = WalkerHandler.__add_walker( base_image=layer, walker=walker_asset, margin=margin )
    return layer

  def get_walker_asset( base_image: ImageType ) -> ImageType:
    self = WalkerHandler
    asset_url = CFG.ASSETS_BASE_URL + CFG.WALKER_ASSET_NAME
    try:
      with urllib.request.urlopen(asset_url) as url:
        img = Image.open(url)
        return img

    except Exception as err:
      ErrLog.log( err )
      return self.__get_walker_asset_fallback( base_image=base_image )

  def __get_walker_asset_fallback( base_image: ImageType ) -> ImageType:
    try:
      walker = Image.open( CFG.WALKER_ASSET_PATH )
      walker = img_resize.resize_by_height( origin=walker, dest=base_image )
      return walker

    except Exception as err:
      ErrLog.log( err )
      return Image.new( mode='RGB', size=(60,120), color='black' )

  def __add_walker( base_image: ImageType, walker: ImageType, margin: int ) -> ImageType:

    base_w, base_h = base_image.size
    walker_w, walker_h = walker.size
    paste_w = base_w - walker_w - margin
    paste_h = base_h - walker_h - margin
    offset = ( paste_w, paste_h )

    try:
      base_image.paste( walker, offset, walker )
      return base_image

    except Exception as err:
      ErrLog.log( err )
      return base_image
