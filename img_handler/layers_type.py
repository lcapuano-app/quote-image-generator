from typing import TypedDict
from PIL.Image import Image as ImageType

class BaseLayers( TypedDict ):
  bkg           : ImageType
  decor         : ImageType
  margin        : int
  walker        : ImageType
  waleker_asset : ImageType

class QuoteLayers( BaseLayers ):
  author_img  : ImageType
  author_name : ImageType
  quote_text  : ImageType
