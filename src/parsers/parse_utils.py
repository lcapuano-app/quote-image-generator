import logging
from PIL import ImageColor

from definitions import COLOR_TRANSPARENT


_logger = logging.getLogger(__name__)


def to_rgba( color: str, default: str = COLOR_TRANSPARENT, mode: str = None ) -> str:

    if mode is None:
        mode = 'RGBA'
    else:
        mode = mode.upper()
        mode = mode if mode == 'RGBA' or mode == 'RGB' else 'RGBA'

    if not isinstance( color, str ):
        return default
    
    try:
        parsed_val: str = ImageColor.getcolor( color, mode )
        prefix: str = mode.lower()
        return f"{prefix}{parsed_val}"

    except Exception as err:
        _logger.error(err)
        return default