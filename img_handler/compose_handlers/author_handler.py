import urllib.request
from typing import Tuple
from PIL import Image, ImageOps
from PIL.Image import Image as ImageType
from config import CFG
from error_log import ErrLog

class AuthorHandler():

  def get_author_layer( base_img: Image, image_src: str ) -> ImageType:
    author_asset = AuthorHandler.__get_author_image( image_src=image_src )
    author_asset = AuthorHandler.__author_resize( base_img=base_img, author_img=author_asset )
    author_asset = ImageOps.grayscale( image=author_asset )
    author_asset = author_asset.rotate( angle=CFG.AUTHOR_ROTATE_ANGLE, expand=0, center=None, translate=None, fillcolor=None )
    author_asset = AuthorHandler.__author_crop( base_img=base_img, author_img=author_asset )
    author_asset.putalpha( CFG.AUTHOR_IMG_ALPHA )

    return author_asset

  def __get_author_image( image_src: str ):
    asset_url = CFG.ASSETS_BASE_URL + image_src + CFG.IMG_EXT

    try:
      with urllib.request.urlopen(asset_url) as url:
        img = Image.open(url)
        return img

    except Exception as err:
      ErrLog.log( err )
      return AuthorHandler.__get_author_image_fallback( image_src=image_src )

  def __get_author_image_fallback( image_src: str ) -> ImageType:

    try:
      author_asset = Image.open( CFG.SRC_DIR + image_src + CFG.IMG_EXT )
      return author_asset

    except Exception as err:
      ErrLog.log( err )
      return AuthorHandler.__get_author_default_img()

  def __get_author_default_img() -> ImageType:
    try:
      return Image.open( CFG.AUTHOR_IMG_FALLBACK )
    except Exception as err:
      ErrLog.log( err )
      return Image.new( mode='RGB', size=CFG.IMG_SIZE, color='black' )

  def __author_crop( base_img: Image, author_img: Image) -> ImageType:
    author_w, author_h = author_img.size
    base_w, base_h = base_img.size

    crop_w = (author_w - base_w) // 2
    crop_h = (author_h - base_h) // 2
    crop_border = ( crop_w, crop_h, crop_w, crop_h ) #(left, top, right, bottom)

    author_img = ImageOps.crop( image=author_img, border=crop_border )
    return author_img

  def __author_resize( base_img: Image, author_img: Image ) -> ImageType:
    author_size = author_img.size
    base_size = base_img.size
    img_size = AuthorHandler.__resize_it( author_size=author_size, base_size=base_size )
    return author_img.resize( img_size, Image.Resampling.BILINEAR )

  def __resize_it(  author_size: Tuple[ int, int ], base_size: Tuple[ int, int ] ) -> Tuple[int, int]:
    author_w, author_h = author_size
    base_w, base_h = base_size

    lim_h = base_h * CFG.AUTHOR_RESIZE_LIMIT_RATIO
    lim_w = base_w * CFG.AUTHOR_RESIZE_LIMIT_RATIO
    limit_size = ( lim_w, lim_h )

    if author_w >= lim_w and author_h >= lim_h:
      return AuthorHandler.__decrese_it( author_w, author_h, base_w, base_h, lim_w, lim_h )
    else:
      return AuthorHandler.__increse_it( author_size=author_size, base_size=base_size, limit_size=limit_size )

  def __decrese_it( author_size: Tuple[ int, int ], base_size: Tuple[ int, int ], limit_size: Tuple[ int, int ] ) -> Tuple[int, int]:
    author_w, author_h = author_size
    base_w, base_h = base_size
    lim_w, lim_h = limit_size

    quo_w = base_w / author_w
    quo_h = base_h / author_h

    ratio = 1

    if quo_h > quo_w:
      ratio = (lim_w - author_w ) / author_w
    else:
      ratio = (lim_h - author_h ) / author_h

    author_h = round( author_h * ( 1 + ratio ) )
    author_w = round( author_w * ( 1 + ratio ) )

    return author_w, author_h

  def __increse_it( author_size: Tuple[ int, int ], base_size: Tuple[ int, int ], limit_size: Tuple[ int, int ] ) -> Tuple[int, int]:
    author_w, author_h = author_size
    base_w, base_h = base_size
    lim_w, lim_h = limit_size

    quo_w = base_w / author_w
    quo_h = base_h / author_h

    ratio = 1

    if quo_h > quo_w:
      ratio = (lim_h - author_h ) / author_h
    else:
      ratio = (lim_w - author_w ) / author_w

    author_h = round( author_h * ( 1 + ratio ) )
    author_w = round( author_w * ( 1 + ratio ) )

    return author_w, author_h
