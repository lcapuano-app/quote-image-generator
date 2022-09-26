from dataclasses import dataclass
from typing import Tuple

from models.def_author import AuthorDefs
from models.def_quote import QuoteDefs
from models.def_decor import DecorDefs
from definitions import (
    ASSETS_URL,
    AUTHOR_IMG_ALPHA,
    AUTHOR_RESIZE_LIMIT_RATIO,
    AUTHOR_ROTATE_ANGLE,
    COLOR_AUTHOR,
    COLOR_BG,
    COLOR_DECOR,
    COLOR_QUOTE,
    COLOR_STROKE,
    FONT_FACE,
    FONT_AUTHOR_SCALE_FACTOR,
    FONT_QUOTE_SCALE_FACTOR,
    QUOTE_STROKE_SIZE,
    IM_MARGIN_RATIO,
    IM_REQ_AUTHOR_NAME,
    IM_REQ_AUTHOR_IMG_NAME,
    IM_REQ_QUOTE_ID,
    IM_REQ_QUOTE_TEXT,
    IM_REQ_SIZE,
    TEXT_MULTI_WRAP
)



## REQUEST
@dataclass( slots=True )
class ImReqOptions:
    assets_url: str = ASSETS_URL
    color_bkg: str = COLOR_BG
    color_decor: str = COLOR_DECOR
    margin_ratio: float = IM_MARGIN_RATIO


@dataclass( slots=True )
class ImRequest:

    author: AuthorDefs = AuthorDefs()
    decor: DecorDefs = DecorDefs()
    im_size: Tuple[int, int] = IM_REQ_SIZE
    options: ImReqOptions = ImReqOptions()
    quote: QuoteDefs = QuoteDefs()