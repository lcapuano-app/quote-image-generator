import logging
import pathlib
import requests
import os

from pathlib import Path
from typing import Dict
from PIL.Image import Image
from PIL import Image as Im

from result import Result, Ok, Err, Some
from definitions import EXT_API_SAVE_QUOTE_URL, EXT_API_OUTPUT_URL
from imgen.imgen import ImRequest


_logger = logging.getLogger(__name__)


class QuoteImUtils:

    @staticmethod
    def parse_req_dict( some_dict: Dict ) -> ImRequest:

        try:
            errs, validated = ImRequest.parser(some_dict)
            validated.errs = errs

            return validated

        except Exception as err:
            _logger.error( err, exc_info=True )
            im_req = ImRequest()
            im_req.errs = [err]
            return im_req 

    
    @staticmethod
    def send_to_ext_api( filename: str , filepath: str, default_url: str ) -> Result[str, Exception]:
        s_key: str = os.environ['API_SECRET_KEY']
        s_value: str = os.environ['API_SECRET_VAL']
        url = f'{EXT_API_SAVE_QUOTE_URL}?{s_key}={s_value}'

        try:
            with open( filepath, 'rb' ) as im_file:
                from PIL import Image as Im
                payload={}
                files=[( 'quote', (filename , im_file, 'image/png') )]
                headers = { 
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                }
                response = requests.post( url, headers=headers, data=payload, files=files)

                if response and response.status_code == 200:
                    im_url: str = f'{EXT_API_OUTPUT_URL}/{filename}'
                    return Ok( im_url )
                else:
                    _logger.warn( response.headers )
                    _logger.warn( response.text )
                    _logger.warn( f'"{url}"' )
                    im_url: str = f'{EXT_API_OUTPUT_URL}/default.png'
                    return Some(default_url)
        
        except Exception as err:
            _logger.error(err, exc_info=True)
            return Err(err)


    @staticmethod
    def save_im_as( img: Image, filename: str , filepath: str ) -> Result[None, Exception]:

        keep_alpha: bool = False

        if img is None:
            return Err( ValueError('Image is None') )

        try:
            file_extension = pathlib.Path(filename).suffix
            keep_alpha = file_extension == '.png' or  file_extension == '.PNG'
        except Exception:
            keep_alpha = False

        try:
            im_clone = img

            if not keep_alpha:
                im_clone = im_clone.convert('RGB')

            im_clone.save( filepath )
            return Ok( None )

        except Exception as err:
            _logger.error( err, exc_info=True )
            return Err( err )


    @staticmethod
    def save_im_as_b64( filename: str , filepath: str, default_url: str ):
        pass


    @staticmethod
    def send_to_ext_api_b64( filename: str , filepath: str, default_url: str ):
        (800,600)
    

    @staticmethod
    def img_already_exists_ext_api( filename: str ) -> bool:
        url: str = f'{EXT_API_OUTPUT_URL}/{filename}'
        headers = { 
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        try:
            response = requests.get( url, headers=headers )
            return response.status_code == 200

        except Exception as err:
            _logger.error(err)
            return False


    @staticmethod
    def img_already_exists_local( filepath: str ) -> bool:
        path = Path(filepath)
        return path.is_file()
