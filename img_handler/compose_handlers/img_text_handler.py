from typing import Any, Tuple
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType

class ImgTextHandler():

  font_size_quote = 22
  font_size_author = 26
  font_factor = 0.0275

  def get_text_layer( size: Tuple[ int, int ]=(800,600) ) -> ImageType:
    self = ImgTextHandler
    layer = Image.new( mode='RGBA', size=size, color='rgba(0,0,0,0)' )
    self.__set_fonts_sizes( size[0] )
    return layer

  def add_text(
    base_img: Image,
    type: str,
    text: str,
    color: str,
    margin: int,
    font: str,
    walker_asset: Image = None ) -> ImageType:


    draw = ImageDraw.Draw( im=base_img )
    font_tt = None
    pos = (0,0)

    if type == 'author':
      font_tt = ImageFont.truetype( font=font, size=ImgTextHandler.font_size_author )
      pos = ImgTextHandler.__get_author_name_x_y( author_name=text, base_img=base_img, font=font_tt, margin=margin, walker=walker_asset )
    else:
      font_tt = ImageFont.truetype( font=font, size=ImgTextHandler.font_size_quote )


    draw = ImageDraw.Draw( im=base_img )

    draw.text( xy=pos, text=text, fill=color, font=font_tt, align='right')

    return base_img

  def __set_fonts_sizes( width: int ) -> None:
    self = ImgTextHandler

    quote = int( width * self.font_factor )
    author = quote + 4

    self.font_size_author = author
    self.font_size_quote = quote
