from typing import Any, Tuple
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from .img_text_handler import ImgTextHandler as ImgText
from ..layers_type import QuoteLayers

class ImgTextAuthorHandler( ImgText ):

  def add_name_layer( quote_layers: QuoteLayers, text: str, color: str, font: str ) -> QuoteLayers:
    self = ImgTextAuthorHandler

    walker = quote_layers['waleker_asset']
    margin = quote_layers['margin']
    size = quote_layers['bkg'].size

    layer = self.get_text_layer( size=size )
    layer = self.__add_author_name( layer=layer, text=text, color=color, margin=margin, font=font, walker=walker )

    quote_layers['author_name'] = layer

    return quote_layers

  def __add_author_name( layer: Image, text: str, color: str, margin: int, font: str, walker: Image ) -> ImageType:
    self = ImgTextAuthorHandler

    draw = ImageDraw.Draw( im=layer )
    font_tt = ImageFont.truetype( font=font, size=self.font_size_author )
    pos = self.__get_author_name_pos( author_name=text, base_img=layer, font=font_tt, margin=margin, walker=walker )
    align = 'right'

    draw.text( xy=pos, text=text, fill=color, font=font_tt, align=align)

    return layer

  def __get_author_name_pos( author_name: str, base_img: Image, font: Any, margin: int, walker: Image ) -> Tuple[int, int]:
    self = ImgTextAuthorHandler

    txt_w, txt_h = ImageDraw.Draw( im=base_img ).textsize( text=author_name, font=font )
    img_w, img_h = base_img.size
    walker_w, walker_h = walker.size
    font_size = self.font_size_author

    x = img_w - txt_w - font_size - walker_w - margin
    y = img_h - txt_h - font_size - margin

    return int(x), int(y)
