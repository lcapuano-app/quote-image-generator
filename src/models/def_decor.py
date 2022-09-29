import logging
from dataclasses import dataclass
from typing import Dict

from parsers import parse_utils
from definitions import COLOR_DECOR


_logger = logging.getLogger(__name__)


@dataclass( slots=True )
class DecorDefs:
    color: str = COLOR_DECOR
    line_height: int = None

    @staticmethod
    def parser( some_dict: Dict ):

        errs = []
        defs = DecorDefs()

        if not isinstance( some_dict, dict ):
            err = ValueError('Not instance of dict')
            errs.append(err)
            return errs, defs

        for key in DecorDefs.__annotations__:
            some_dict_value = some_dict.get(key)

            if some_dict_value is not None:

                if key == 'color':
                    some_dict_value = parse_utils.to_rgba( color=some_dict_value, default=COLOR_DECOR )

                try:
                    some_type = type(getattr( defs, key ))
                    parsed_value = some_type(some_dict_value)
                    setattr(defs, key, parsed_value )
                except Exception as err:
                    errs.append(err)
                    _logger.warning( err )

        return errs, defs