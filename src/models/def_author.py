from dataclasses import dataclass
import logging

from typing import Dict

from parsers import parse_utils
from definitions import (
    AUTHOR_IMG_ALPHA,
    AUTHOR_RESIZE_LIMIT_RATIO,
    AUTHOR_ROTATE_ANGLE,
    COLOR_AUTHOR,
    FONT_FACE,
    FONT_AUTHOR_SCALE_FACTOR,
    IM_REQ_AUTHOR_NAME,
    IM_REQ_AUTHOR_IMG_NAME,
)


_logger = logging.getLogger(__name__)


@dataclass( slots=True )
class AuthorOptions:
    font_face: str = FONT_FACE
    font_color: str = COLOR_AUTHOR
    font_size: int = 0
    font_size_factor: float = FONT_AUTHOR_SCALE_FACTOR
    im_alpha: int = AUTHOR_IMG_ALPHA
    im_resize_limit_ratio: float = AUTHOR_RESIZE_LIMIT_RATIO
    im_rotate_degs: float = AUTHOR_ROTATE_ANGLE

    @staticmethod
    def parser( some_dict: Dict ):
       
        options = AuthorOptions()

        if not isinstance( some_dict, dict ):
            return options
             
        for key in AuthorOptions.__annotations__:

            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:

                if key == 'font_color':
                    some_dict_value = parse_utils.to_rgba( color=some_dict_value, default=COLOR_AUTHOR )

                if type(some_dict_value) == AuthorOptions.__annotations__.get(key):
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
class AuthorDefs:
    name: str = IM_REQ_AUTHOR_NAME
    img_name: str = IM_REQ_AUTHOR_IMG_NAME
    options: AuthorOptions = AuthorOptions()

    @staticmethod
    def parser( some_dict: Dict ):
        
        errs = []
        defs = AuthorDefs()
    
        if not isinstance( some_dict, dict ):
            err = ValueError('Not instance of dict')
            errs.append(err)
            return errs, defs
             
        for key in AuthorDefs.__annotations__:
            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:
                if key == 'options':
                    opts = AuthorOptions.parser( some_dict_value )
                    setattr(defs, key, opts )
                else:
                    if type(some_dict_value) == AuthorDefs.__annotations__.get(key):
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
