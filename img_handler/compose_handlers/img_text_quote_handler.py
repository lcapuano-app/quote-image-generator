import textwrap
import math
from typing import Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from .img_text_handler import ImgTextHandler as ImgText
from ..layers_type import QuoteLayers
from config import CFG

class ImgTextQuoteHandler( ImgText ):

  def add_quote_text_layer( quote_layers: QuoteLayers, text: str, color: str, font: str ) -> QuoteLayers:
    self = ImgTextQuoteHandler

    size = quote_layers['bkg'].size

    layer = self.get_text_layer( size=size )
    layer = self.__add_quote_text( layer=layer, text=text, color=color, font=font )

    return layer

  def __add_quote_text( layer: Image, text: str, font: str, color: str, ) -> ImageType:

    self = ImgTextQuoteHandler

    fill = CFG.QUOTE_TXT_RGB
    stroke_fill = CFG.QUOTE_TXT_STROKE
    draw = ImageDraw.Draw( im=layer )
    text, wrapped = self.__adjust_quote_text( text=text )
    font_size = self.__adjust_font_size( img=layer, font=font, text=text, wrapped=wrapped )
    font_tt = ImageFont.truetype( font=font, size=font_size )
    pos = self.__get_quote_text_pos( text=text, base_img=layer, font=font_tt )

    draw = ImageDraw.Draw( im=layer )
    draw.text( xy=pos, text=text, fill=fill, font=font_tt, anchor='ms', align='center', stroke_width=1, stroke_fill=stroke_fill)

    return layer


  def __get_quote_text_pos( text: str, base_img: ImageType, font: Any ) -> Tuple[int, int]:
    self = ImgTextQuoteHandler

    txt_w, txt_h = ImageDraw.Draw( im=base_img ).textsize( text=text, font=font )
    img_w, img_h = base_img.size

    x = img_w // 2
    y =   (img_h - txt_h) // 2

    return x,y

  def __adjust_quote_text( text: str ) -> Tuple[ str, List[str] ]:
    text = '“' + text + '”'
    wrapped = textwrap.wrap( text, CFG.TEXT_MULTI_WRAP )
    text = '\n'.join( wrapped )
    return text, wrapped

  def __adjust_font_size( img: ImageType, font: str, text: str, wrapped: List[str] = None ) -> int:
    self = ImgTextQuoteHandler

    img_x, img_y = img.size
    font_size = self.font_size_quote

    font_tt = ImageFont.truetype( font=font, size=font_size )
    txt_w, txt_h = ImageDraw.Draw( im=img ).textsize( text=text, font=font_tt )

    txt_img_limit = img_x - (img_x // 5)
    safe_font_size = font_size

    if len(wrapped) > 1:
      txt_img_limit = img_x - (img_x // 7)

    while txt_w < txt_img_limit:
      font_tt = ImageFont.truetype( font=font, size=int(font_size) )
      txt_w, txt_h = ImageDraw.Draw( im=img ).textsize( text=text, font=font_tt )

      if txt_w < txt_img_limit:
        safe_font_size = font_size

      font_size *= 1.1

    return math.ceil(safe_font_size)
