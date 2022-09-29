import logging
from dataclasses import dataclass
from turtle import width
from typing import Any, Dict, List, Tuple

from parsers import parse_utils
from models.def_author import AuthorDefs
from models.def_quote import QuoteDefs
from models.def_decor import DecorDefs
from definitions import (
    EXT_API_ASSETS_URL,
    COLOR_BG,
    COLOR_DECOR,
    IM_MARGIN_RATIO,
    IM_REQ_SIZE,
)


_logger = logging.getLogger(__name__)


@dataclass( slots=True )
class ImReqOptions:
    assets_url: str = EXT_API_ASSETS_URL
    color_bkg: str = COLOR_BG
    color_decor: str = COLOR_DECOR
    margin_ratio: float = IM_MARGIN_RATIO

    @staticmethod
    def parser( some_dict: Dict ):
       
        options = ImReqOptions()

        if not isinstance( some_dict, dict ):
            return options
             
        for key in ImReqOptions.__annotations__:

            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:

                if key == 'color_bkg':
                    some_dict_value = parse_utils.to_rgba( color=some_dict_value, default=COLOR_BG )

                if key == 'color_decor':
                    some_dict_value = parse_utils.to_rgba( color=some_dict_value, default=COLOR_DECOR )

                if type(some_dict_value) == ImReqOptions.__annotations__.get(key):
                    setattr(options, key, some_dict_value )                    
                else:
                    try:
                        some_type = type(getattr( options, key ))
                        parsed_value = some_type(some_dict_value)
                        setattr(options, key, parsed_value )
                    except Exception as err:
                        _logger.warning( err )
 
        return options


@dataclass( slots=True )
class ImRequest:

    author: AuthorDefs = AuthorDefs()
    decor: DecorDefs = DecorDefs()
    im_size: Tuple[int, int] = IM_REQ_SIZE
    options: ImReqOptions = ImReqOptions()
    quote: QuoteDefs = QuoteDefs()

    errs: List[Any] = None


    @staticmethod
    def parser( some_dict: Dict ):

        errs: List = []
        defs = ImRequest()

        if not isinstance( some_dict, dict ):
            err = ValueError('Not instance of dict')
            errs.append(err)
            return errs, defs

        for key in ImRequest.__annotations__:

            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:

                if key == 'author':
                    author_errs, opts = AuthorDefs.parser( some_dict_value )
                    setattr(defs, key, opts )
                    errs = errs + author_errs

                elif key == 'decor':
                    decor_errs, opts = DecorDefs.parser( some_dict_value )
                    setattr(defs, key, opts )
                    errs = errs + decor_errs

                elif key == 'quote':
                    quote_errs, opts = QuoteDefs.parser( some_dict_value )
                    setattr(defs, key, opts )
                    errs = errs + quote_errs

                elif key == 'options':
                    opts = ImReqOptions.parser( some_dict_value )
                    setattr(defs, key, opts )

                elif key == 'size':
                    try:
                        width, height = some_dict_value
                        width = int(width)
                        height = int(height)
                        setattr(defs, key, (width, height) )

                    except Exception as err:
                        errs.append(err)
                   
                

        return errs, defs