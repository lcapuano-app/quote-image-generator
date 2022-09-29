import logging
import pathlib
import requests

from dataclasses import dataclass
import os
from typing import Dict, Tuple
from PIL.Image import Image

from result import Result, Ok, Err, Some
from definitions import TEMP_DIR, EXT_API_SAVE_QUOTE_URL, EXT_API_OUTPUT_URL
from imgen.imgen import ImGen
from imgen.imgen_utils import ImGenUtils
from models.im_request import ImRequest
from quote_im.qt_im_utils import QuoteImUtils


_logger = logging.getLogger(__name__)


@dataclass( slots=True )
class GetQuoteIm:

    req_dict: Dict
    im_req: ImRequest
    
    def __init__(self, req_dict: Dict ) -> None:
        self.req_dict = req_dict


    def create_and_save( self ) -> Result[Tuple[str, str, ImRequest], Exception]:
        """" 
        Creates an saves a quote image.

        First it will parse de quote request dict to a valid `ImRequest`. 
        Then it checks if the image already exisits on external api and local.
        If exists in both it just returns otherwise it will create where is missing (external, local or both)
        :returns `Ok|Some[tuple[filepath, fileurl, ImRequest]] | Err[Exception]`
        """
        self.im_req = QuoteImUtils.parse_req_dict(  self.req_dict )
        filename: str = self.get_filename()
        filepath: str = os.path.join( TEMP_DIR, filename )
        fallback_url: str = f'{EXT_API_OUTPUT_URL}/default.png'
        ext_api_im_url: str = f'{EXT_API_OUTPUT_URL}/{filename}'
        exists_on_api: bool = QuoteImUtils.img_already_exists_ext_api( filename )
        exists_on_local: bool = QuoteImUtils.img_already_exists_local( filepath )
        img: Image = None

        if exists_on_api and exists_on_local:
            return Ok(( filepath, ext_api_im_url, self.im_req ))

        elif exists_on_local and not exists_on_api:
            im_url = QuoteImUtils.send_to_ext_api( 
                filename, filepath, fallback_url ).unwrap_or( fallback_url )
            return Ok(( filepath, im_url, self.im_req ))

        elif exists_on_api and not exists_on_local:
            match ImGenUtils.get_im_by_url( ext_api_im_url ):
                case Ok( res_img ): img = res_img
                case Err(_): img = ImGen( self.im_req ).gen_quote().unwrap_or(None)

        else: 
            img = ImGen( self.im_req ).gen_quote().unwrap_or(None)


        match QuoteImUtils.save_im_as(img, filename, filepath ):
            case Err( _ ):
                return Some(( None, fallback_url, self.im_req ))
            case Ok():                
                im_url = QuoteImUtils.send_to_ext_api( 
                    filename, filepath, fallback_url ).unwrap_or( fallback_url )
                return Ok(( filepath, im_url, self.im_req ))


    def get_filename( self ) -> str:
        try:
            w, h = self.im_req.im_size
            return f'{self.im_req.quote.quote_id}-{w}x{h}.jpg'

        except Exception as err:
            _logger.error(err, exc_info=True )
            return f'{self.im_req.quote.quote_id}.jpg'

    
