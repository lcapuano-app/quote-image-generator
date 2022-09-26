from dataclasses import dataclass

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


@dataclass( slots=True )
class AuthorOptions:
    font_face: str = FONT_FACE
    font_color: str = COLOR_AUTHOR
    font_size: int = 0
    font_size_factor: float = FONT_AUTHOR_SCALE_FACTOR

    im_alpha: int = AUTHOR_IMG_ALPHA
    im_resize_limit_ratio: float = AUTHOR_RESIZE_LIMIT_RATIO
    im_rotate_degs: float = AUTHOR_ROTATE_ANGLE


@dataclass( slots=True )
class AuthorDefs:
    name: str = IM_REQ_AUTHOR_NAME
    img_name: str = IM_REQ_AUTHOR_IMG_NAME
    options: AuthorOptions = AuthorOptions()

