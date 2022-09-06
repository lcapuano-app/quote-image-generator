from typing import Tuple
from PIL import Image
from .background_handler import BackgroundHandler as Background
from .bottom_decor_handler import BottomDecorHandler as Decor
from .walker_handler import WalkerHandler as Walker
from ..layers_type import BaseLayers
from config import CFG

class BaseImgHandler():

  __margin = 0
  __gold_rgb = ''

  def __init__(self, gold_rgb) -> None:
    BaseImgHandler.__gold_rgb = gold_rgb

  def get_base_layers( self, mode: str, size: Tuple[ int, int ], color: str ) -> BaseLayers:
    handler = BaseImgHandler

    bkg_layer = Background.create_background( mode=mode, size=size, color=color )
    handler.__set_margin( base_img=bkg_layer )

    walker_asset = Walker.get_walker_asset( base_image=bkg_layer )
    walker_layer = Walker.get_walker_layer( walker_asset=walker_asset, size=size, margin=self.__margin )

    decor_layer = Decor.get_decor_layer( size=size, walker=walker_asset, color=self.__gold_rgb, margin=self.__margin )

    #return bkg_layer, walker_layer, decor_layer, walker_asset, handler.__margin
    return {
      'bkg': bkg_layer,
      'decor': decor_layer,
      'margin': handler.__margin,
      'walker': walker_layer,
      'waleker_asset': walker_asset
    }

  def __set_margin( base_img: Image ):
    w, h = base_img.size
    if w > h:
      BaseImgHandler.__margin = int(h * CFG.MARGIN_RATIO)
    else:
      BaseImgHandler.__margin = int(w * CFG.MARGIN_RATIO)
