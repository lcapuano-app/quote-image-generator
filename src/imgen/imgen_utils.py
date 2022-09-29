import logging
import os
import urllib.request

from typing import Tuple
from PIL import Image as Im
from PIL.Image import Image

from result import Result, Ok, Err
from definitions import ASSETS_DIR, COLOR_TRANSPARENT, IM_WIDTH, IM_HEIGHT, IM_MODE, EXT_API_ASSETS_URL, FONT_QUOTE_SCALE_FACTOR


_logger = logging.getLogger(__name__)


class ImGenUtils:

    @staticmethod
    def im_new( size: Tuple[int, int] = None, color: str = None ) -> Result[Image, Exception]:

        color = color if color is not None else COLOR_TRANSPARENT
        size = size if size is not None else ( IM_WIDTH, IM_HEIGHT )

        try:
            im = Im.new( IM_MODE, size, color )
            return Ok(im)
        except Exception as err:
            return Err(err)


    @staticmethod
    def get_margin( *, width: int, height: int, ratio: int = 1 ) -> int:
        """ Calcs the margin (w, h, t, b) in pixels """
        if width > height:
            return int(height * ratio)
        else:
            return int(width * ratio)


    @staticmethod
    def get_im_by_dir( filename: str, dirname: str ) -> Result[Image, Exception]:
        """ Loads an image from a given local path """
        try:
            filepath = os.path.join(dirname, filename)
            asset = Im.open( filepath )
            return Ok( asset )

        except Exception as err:
            return Err( err )


    @staticmethod
    def get_im_by_url( url: str, save_as: Tuple[str, str] = None ) -> Result[Image, Exception]:
        """ Loads an image from a given URL.
        :`save_as` (dir, filename). If is set saves the result to `dir/filename.ext`"""
        print('URL')
        try:
            with urllib.request.urlopen(url) as im_file:
                walker: Image = Im.open(im_file)

                if save_as is not None:
                    dirname, filename = save_as
                    file_path: str = os.path.join(dirname, filename)
                    walker.save(file_path)

                return Ok( walker )

        except Exception as err:
            return Err(f'{url}: {err}')


    @staticmethod
    def get_im_with_fallback(*, filename: str = None, dirname: str = None, url: str = None ) -> Result[Image, Exception]:
        """ 
            Tries to grab an image in 2 steps. It only goes to the next step if the previus has failed
            :1. Directly from local storage.
            :2. From a given url. If url is none it will get one using the default api url + filename
        """
        dirname = dirname if dirname is not None else ASSETS_DIR
        url = url if url is not None else f'{EXT_API_ASSETS_URL}{filename}'
       
        match ImGenUtils.get_im_by_dir( filename, dirname ):
            case Ok( img ): 
                return Ok(img)
            case Err( err ):
                _logger.warn( err )
                match ImGenUtils.get_im_by_url( url, save_as = (dirname, filename) ):
                    case Ok( img ):
                        return Ok(img)
                    case Err( err ):
                        return Err( err )

    
    @staticmethod
    def resize_im_by_percentage( img: Image, percentage: float ) -> Image:
        """ Resizes an image by some percentage """
        width, height = img.size
        resized_dimensions = (int(width * percentage), int(height * percentage))
        resized = img.resize(resized_dimensions)
        return resized


    @staticmethod
    def resize_im_by_height( *, origin: Image, dest: Image, proportion: float = 1/5 ) -> Image:
        """ Resizes an image by its destination height size """
        _, origin_h = origin.size
        _, dest_h = dest.size
        img_h = int(dest_h * proportion)
        ratio = 1

        if origin_h > img_h:
            ratio =  1 + ( (origin_h - img_h) / img_h )
        else:
            ratio =  1 + ((img_h - origin_h) / origin_h)

        return ImGenUtils.resize_im_by_percentage( origin, ratio )

    
    @staticmethod
    def resize_over_bkg_size(*, bkg: Image, origin: Image, factor: float = 1.0 ) -> Result[Image, Exception]:

        try:
        
            origin_w, origin_h = origin.size
            bkg_w, bkg_h = bkg.size

            lim_h: float = abs(bkg_h * factor)
            lim_w: float = abs(bkg_w * factor)

            quo_w = bkg_w / origin_w
            quo_h = bkg_h / origin_h

            ratio = 1

            if origin_w >= lim_w and origin_h >= lim_h:
                # decrase it
                if quo_h > quo_w:
                    ratio = (lim_w - origin_w ) / origin_w
                else:
                    ratio = (lim_h - origin_h ) / origin_h
            else:
                if quo_h > quo_w:
                    ratio = (lim_h - origin_h ) / origin_h
                else:
                    ratio = (lim_w - origin_w ) / origin_w


            size_h: int = round( origin_h * ( 1 + ratio ) )
            size_w: int = round( origin_w * ( 1 + ratio ) )
            size: Tuple[int, int] = ( size_w, size_h )

            resized: Image = origin.resize( size, Im.Resampling.BILINEAR )
            return Ok(resized)

        except Exception as err:
            return Err( err )

    
    @staticmethod
    def scale_font_size(*, font_size: int, canvas_w: int, factor: float ):

        try:
            font_size = abs(font_size) if isinstance( font_size, int ) else 0
            canvas_w = abs(canvas_w) if isinstance( canvas_w, int ) else IM_WIDTH
            factor = abs(factor) if isinstance( factor, float ) else FONT_QUOTE_SCALE_FACTOR
            
            if font_size > 0:
                return font_size
            else:
                return int( canvas_w * factor )

        except Exception as err:
            _logger.error(err, exc_info=True)
            return abs(font_size)

        