import dataclasses
import json
import logging

from http.server import SimpleHTTPRequestHandler
from pprint import pp
from typing import Dict, List, Tuple

from result import Result, Ok, Err, Some
from imgen.imgen import ImGen
from quote_im.get_im import GetQuoteIm
from models.im_request import ImRequest


_logger = logging.getLogger(__name__)


def get_help_json() -> Result[str, Exception]:

    base_req = ImRequest()

    try:
        as_dict = dataclasses.asdict(base_req) 
        json_str: str = json.dumps(as_dict, ensure_ascii=False)
        return Ok(json_str)

    except Exception as err:
        _logger.error( err, exc_info=True )
        return Err(err)


def create_quote_img( handler: SimpleHTTPRequestHandler ):

    dict_body: Dict = get_body( handler ).unwrap_or(None)

    if dict_body is None:
        return

    res_filepath: str = None
    res_fileurl: str = None
    res_errors: List = None
    res_setup: Dict = dict_body
    res_create: Tuple[str, str, Dict ] = (res_filepath, res_fileurl, res_setup)

    match GetQuoteIm( dict_body ).create_and_save():
        case Ok( res ) | Some( res ):
            filepath, fileurl, im_req = res
            res_filepath = filepath
            res_fileurl = fileurl
            res_errors = im_req.errs
            res_setup = dataclasses.asdict(im_req)
            
        case Err( err ):
            res_errors = [ err ]

    resp: Dict = {
        "filepath" : res_filepath,
        "fileurl"  : res_fileurl,
        "errors"   : res_errors,
        "setup"    : res_setup
    }

    try:
        json_str: str = json.dumps(resp, ensure_ascii=False)
        return Ok(json_str)

    except Exception as err:
        _logger.error( err, exc_info=True )
        return Err(err)


def get_body( handler: SimpleHTTPRequestHandler ) -> Result[Dict, Exception]:

    try:
        content_length: int = int( handler.headers['Content-Length'] )
        post_data: bytes = handler.rfile.read(content_length)

        if not post_data:
            return Err(ValueError('Empty post body'))

        data: Dict = json.loads(post_data.decode('utf-8'))

        return Ok(data)

    except Exception as err:
        _logger.error( err, exc_info=True )
        return Err(err)


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


def img_from_post( im_req: ImRequest ):
    match ImGen( im_req ).gen_quote():
        case Ok( img):
            print( 'PASSOU')
            img.show()
        case Err( err ):
            print(err)