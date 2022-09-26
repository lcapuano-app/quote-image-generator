from dataclasses import dataclass

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


@dataclass( slots=True )
class QuoteOptions:
    font_face: str = FONT_FACE
    font_color: str = COLOR_QUOTE
    font_size: int = 0
    font_size_factor: float = FONT_QUOTE_SCALE_FACTOR
    stroke_size: int = QUOTE_STROKE_SIZE
    stroke_color: str = COLOR_STROKE
    text_wrap: int = TEXT_MULTI_WRAP


@dataclass( slots=True )
class QuoteDefs:
    options: QuoteOptions = QuoteOptions()
    quote_id: str = IM_REQ_QUOTE_ID
    quote_text: str = IM_REQ_QUOTE_TEXT

