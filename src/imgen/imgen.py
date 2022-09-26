import logging

from typing import Tuple
from PIL.Image import Image

from result import Result, Ok, Err, Some
from imgen.imgen_utils import ImGenUtils
from definitions import FALLBACK_DIR
from models.im_request import ImRequest
from imgen.layers import author, background, decor, quote, walker


_logger = logging.getLogger(__name__)


class ImGen:

    margin: int = 0
    
    
    def __init__( self, im_req: ImRequest = None ) -> None:

        self.im_req = im_req if im_req is not None else ImRequest()

        width, height = self.im_req.im_size
        self.margin = ImGenUtils.get_margin( 
            width=width, height=height, ratio=self.im_req.options.margin_ratio )
        
    
    def gen_quote( self ) -> Result[Image, Exception]:

        base_img: Image = None
        walker_asset: Image = None

        match self.bkg_create():
            case Ok( bkg ): base_img = bkg
            case Some( err_dflt ): return Ok( err_dflt )
            case Err( err ): return Err(err)

        match self.walker_create_and_paste( base_img ):
            case Ok( wlkr_imgs ): base_img, walker_asset = wlkr_imgs
            case Some( some_base_img ): base_img = some_base_img
            case Err( err ): return Err(err)


        if walker_asset:
            match self.decor_create_and_paste( walker_asset, base_img ):
                case Ok( layer ): base_img = layer
                case Some( some_base_img ): base_img = some_base_img
                case Err( err ): return Err(err)

        match self.author_create_and_paste( base_img, walker_asset ):
            case Ok( layer ): base_img = layer
            case Err( err ): return self.fatal_error_default(err)


        match self.quote_create_and_paste( base_img ):
            case Ok( layer ): base_img = layer
            case Err( err ): return self.fatal_error_default(err)
        

        return Ok(base_img)
    
    
    def bkg_create( self ) -> Result[Image, Exception]:
        
        bkg_response = background.create( 
            size = self.im_req.im_size, 
            img_name = self.im_req.author.img_name,
            color = self.im_req.options.color_bkg, 
            resize_factor = self.im_req.author.options.im_resize_limit_ratio,
            rotate_deg = self.im_req.author.options.im_rotate_degs,
            img_alpha = self.im_req.author.options.im_alpha 
        )

        match bkg_response:
            case Ok( bkg ): return Ok(bkg)
            case Err( err ):
                match self.fatal_error_default(err):
                    case Ok( err_img ): return Some( err_img )
                    case Err( err ): return Err(err)


    def walker_create_and_paste( self, canvas: Image ) -> Result[Image | Tuple[Image, Image], Exception]:

        walker_layer: Image = None
        walker_asset: Image = None

        match walker.create( size=self.im_req.im_size, margin=self.margin ):
            case Ok( wlkr_res ): walker_layer, walker_asset = wlkr_res
            case Err( err ):
                match self.on_error_get_base( err ):
                    case Ok( fallback_img ): return Some( fallback_img )
                    case Err( err ): return Err(err)
                    

        match self.paste_layers( walker_layer, canvas ):
            case Ok( pasted ): return Ok((pasted, walker_asset))
            case Err( err ): 
                _logger.error(err, stack_info=True )
                return Some( canvas )
    
               
    def decor_create_and_paste( self, walker_asset: Image, canvas: Image ) -> Result[Image, Exception]:

        decor_layer: Image = None
    

        decor_create_resp = decor.create( 
            walker_asset, canvas, margin=self.margin, color=self.im_req.decor.color )

        match decor_create_resp:
            case Ok(layer):  decor_layer = layer
            case Err( err ):
                match self.on_error_get_base( err ):
                    case Ok( fallback_img ): Some(fallback_img)
                    case Err( err ): return Err(err)
                    
        match self.paste_layers( decor_layer, canvas ):
            case Ok( pasted ): return Ok( pasted )
            case Err( err ): 
                _logger.error(err, stack_info=True )
                return Some( canvas )
       

    def author_create_and_paste( self, canvas: Image, walker_asset: Image ) -> Result[Image, Exception]:

        walker_w: int = int()
        author_layer: Image = None

        try:
            walker_w, _ = walker_asset.size

        except Exception as e:
            walker_w, _, err = walker.get_walker_size()
            if err:
                walker_w = self.margin

        create_author = author.create(
            text = self.im_req.author.name,
            size = self.im_req.im_size,
            margin = self.margin,
            font_color = self.im_req.author.options.font_color,
            font_face = self.im_req.author.options.font_face,
            font_size = self.im_req.author.options.font_size,
            walker_w = walker_w
        )

        match create_author:
            case Ok( layer ): author_layer = layer
            case Err(err): return Err(err)

        return self.paste_layers( author_layer, canvas )

    
    def quote_create_and_paste( self, canvas: Image ):

        quote_layer: Image = None

        create_quote = quote.create(
            text = self.im_req.quote.quote_text,
            font_color = self.im_req.quote.options.font_color,
            font_face = self.im_req.quote.options.font_face,
            font_size = self.im_req.quote.options.font_size,
            size = self.im_req.im_size,
            stroke_fill = self.im_req.quote.options.stroke_color,
            stroke_width = self.im_req.quote.options.stroke_size,
            wrap_width = self.im_req.quote.options.text_wrap
        )

        match create_quote:
            case Ok( layer ): quote_layer = layer
            case Err(err): return self.fatal_error_default( err )

        return self.paste_layers( quote_layer, canvas )


    def paste_layers( self, origin: Image, dest: Image, box: Tuple[int, int] = None ) -> Result[Image, Exception]:

        try:
            box = (0, 0) if box is None else box
            dest.paste( origin, box, origin )
            return Ok( dest )

        except Exception as err:
            return Err(err)


    def on_error_get_base( self, err: Exception ) :
        _logger.error( err, exc_info=True )

        fallback_response = ImGenUtils.get_im_with_fallback( 
            filename = 'base.png', dirname = FALLBACK_DIR )

        return fallback_response


    def fatal_error_default(self, err: Exception ) -> Result[Image, Exception]:
        _logger.error(err, exc_info=True, )
        return ImGenUtils.get_im_with_fallback( 
            filename = 'default.png', dirname = FALLBACK_DIR )        

