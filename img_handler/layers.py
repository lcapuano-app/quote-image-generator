import os
from typing import Dict, Tuple
from PIL import Image
from PIL.Image import Image as ImageType
from .compose_handlers import Author, BaseImg, ImgTextAuthor, ImgTextQuote
from quote import QuoteType
from .layers_type import QuoteLayers
from config import CFG

class Layers():

  __margin = 0
  __gold_rgb = CFG.TEXT_COLOR_RGB
  __quote_layers: QuoteLayers = None
  __font_face = CFG.FONT_FACE

  def create_quote_image( quote: QuoteType, output: str, size: Tuple[ int, int ], mode: str='RGB', color: str = 'black' ) -> ImageType:
    self = Layers

    img_name = quote['_id'] + CFG.IMG_EXT
    file_path = os.path.join( output, img_name )

    self.__set_base_layers( mode=mode, size=size, color=color )
    self.__set_author_img_layer( quote=quote )
    self.__set_author_name_layer( quote=quote )
    self.__set_quote_text_layer( quote=quote )

    final_img = self.__merge_layers( file_path=file_path )

    final_img.save( file_path )

    return final_img


  def __set_base_layers( mode: str, size: Tuple[ int, int ], color: str ) -> None:
    self = Layers

    base_layers = BaseImg( gold_rgb= self.__gold_rgb ).get_base_layers( mode=mode, size=size, color=color)
    self.__quote_layers = base_layers
    self.__margin = base_layers['margin']

  def __set_author_img_layer( quote: QuoteType ) -> None:
    self = Layers

    image_src = quote['idName']
    base_img = self.__quote_layers['bkg']
    layer = Author.get_author_layer( base_img=base_img, image_src=image_src )

    self.__quote_layers['author_img'] = layer

  def __set_author_name_layer( quote: QuoteType ) -> None:
    self = Layers

    quote_layers = self.__quote_layers
    text = quote['displayName']
    color = self.__gold_rgb
    font = self.__font_face

    self.__quote_layers = ImgTextAuthor.add_name_layer( quote_layers=quote_layers, text=text, color=color, font=font )

  def __set_quote_text_layer( quote: QuoteType ) -> None:
    self = Layers

    quote_layers = self.__quote_layers
    text = quote['msg']
    color = self.__gold_rgb
    font = self.__font_face

    self.__quote_layers['quote_text'] = ImgTextQuote.add_quote_text_layer( quote_layers=quote_layers, text=text, color=color, font=font )

  def __merge_layers( file_path: str ) -> ImageType:
    self = Layers

    main_img = self.__quote_layers['bkg']
    self.__paste_same_w_h_layers( main_img=main_img, paste_img=self.__quote_layers['author_img'] )
    self.__paste_same_w_h_layers( main_img=main_img, paste_img=self.__quote_layers['walker'] )
    self.__paste_same_w_h_layers( main_img=main_img, paste_img=self.__quote_layers['decor'] )
    self.__paste_same_w_h_layers( main_img=main_img, paste_img=self.__quote_layers['author_name'] )
    self.__paste_same_w_h_layers( main_img=main_img, paste_img=self.__quote_layers['quote_text'] )

    return main_img

  def __paste_same_w_h_layers( main_img: ImageType, paste_img: ImageType ) -> None:
    main_img.paste( paste_img, (0, 0), paste_img )
