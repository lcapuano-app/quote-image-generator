from PIL import Image
from PIL.Image import Image as ImageType
from typing import Tuple

class BackgroundHandler():

  def create_background( mode: str, size: Tuple[ int, int ], color: str ) -> ImageType:
    background = Image.new( mode, size, color )
    return background
