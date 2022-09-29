import logging
from dataclasses import dataclass
from typing import Dict

from parsers import parse_utils
from definitions import (
    COLOR_QUOTE,
    COLOR_STROKE,
    FONT_FACE,
    FONT_QUOTE_SCALE_FACTOR,
    QUOTE_STROKE_SIZE,
    IM_REQ_QUOTE_ID,
    IM_REQ_QUOTE_TEXT,
    TEXT_MULTI_WRAP
)


_logger = logging.getLogger(__name__)


@dataclass( slots=True )
class QuoteOptions:
    font_face: str = FONT_FACE
    font_color: str = COLOR_QUOTE
    font_size: int = 0
    font_size_factor: float = FONT_QUOTE_SCALE_FACTOR
    stroke_size: int = QUOTE_STROKE_SIZE
    stroke_color: str = COLOR_STROKE
    text_wrap: int = TEXT_MULTI_WRAP


    @staticmethod
    def parser( some_dict: Dict ):
       
        options = QuoteOptions()

        if not isinstance( some_dict, dict ):
            return options
             
        for key in QuoteOptions.__annotations__:

            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:

                if key == 'font_color':
                    some_dict_value = parse_utils.to_rgba( color=some_dict_value, default=COLOR_QUOTE )

                if type(some_dict_value) == QuoteOptions.__annotations__.get(key):
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
class QuoteDefs:
    options: QuoteOptions = QuoteOptions()
    quote_id: str = IM_REQ_QUOTE_ID
    quote_text: str = IM_REQ_QUOTE_TEXT

    @staticmethod
    def parser( some_dict: Dict ):

        errs = []
        defs = QuoteDefs()

        if not isinstance( some_dict, dict ):
            err = ValueError('Not instance of dict')
            errs.append(err)
            return errs, defs

        for key in QuoteDefs.__annotations__:
            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:
                if key == 'options':
                    opts = QuoteOptions.parser( some_dict_value )
                    setattr(defs, key, opts )
                else:
                    if type(some_dict_value) == QuoteDefs.__annotations__.get(key):
                        setattr(defs, key, some_dict_value )
                    else:
                        try:
                            some_type = type(getattr( defs, key ))
                            parsed_value = some_type(some_dict_value)
                            setattr(defs, key, parsed_value )
                        except Exception as err:
                            errs.append(err)
                            _logger.warning( err )
            
            else:
                if key != 'options':
                    err = TypeError( f"Mandatory key 'author.{key}' is missing" )
                    errs.append(err)
                    
        return errs, defs