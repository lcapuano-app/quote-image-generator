from typing import Optional, TypedDict
from typing_extensions import NotRequired


class QuoteReqAuthorType( TypedDict ):
    name: str
    img_name: Optional[str]


class QuoteReqType( TypedDict ):
    quote_id   : str
    author     : QuoteReqAuthorType
    quote_text : str
    height     : Optional[int]
    width      : Optional[int]