from dataclasses import dataclass

from definitions import COLOR_DECOR


@dataclass( slots=True )
class DecorDefs:
    color: str = COLOR_DECOR
    line_height: int = None