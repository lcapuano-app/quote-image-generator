from mylib.dict_typing import ImGenReqType
from mylib.utils import validators
from pprint import pprint
from utils import parser, validator


__QUOTE_REQ_FALLBACK: ImGenReqType = {
    "quote_id": "63139372217ba7e20813b92e",
    "author": {
        "name": "Chaves",
        "img_name": "chaves"
    },
    "quote_text": "Volta o cão arrependido, com suas orelhas tão fartas, com seu osso roído e com o rabo entre as patas.",
    "width": 800,
    "height": 600
}


def create_quote_img( quote_req: ImGenReqType ):

    # if quote_req is None:
    #     quote_req = __QUOTE_REQ_FALLBACK
    #print('da erro',quote_req["width"])
    #validator.validate_dict( quote_req, ImGenReqType ).unwrap()
    validators.validate_dict( quote_req, ImGenReqType ).unwrap()
    tt = parser.parse_dict_optionals(quote_req, ImGenReqType )
    pprint(tt)
