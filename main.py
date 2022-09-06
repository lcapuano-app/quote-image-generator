import sys
import upload_quote_img as uploader
from os.path import join, dirname
from typing import List, Tuple
from dotenv import load_dotenv
from cmd_line.cmd_line_args import get_params
from quote import Quote
from img_handler import Layers
from config import CFG

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_quote_id_and_output( argv: List[str] ) -> Tuple[ str, str ]:
  quote_id, output = get_params( argv = sys.argv )

  if len( quote_id ) == 0:
    quote_id = '63139372217ba7e20813b932'
  if len( output ) == 0:
    output = 'output'

  return quote_id, output

def main():
  quote_id, output = get_quote_id_and_output( argv = sys.argv )
  quote = Quote.get_quote( quote_id=quote_id )

  file_name = quote['_id'] + CFG.IMG_EXT
  final_img = Layers.create_quote_image( quote=quote, size=CFG.IMG_SIZE, output=output )

  img_url = uploader.upload_image( final_img=final_img, file_name=file_name )
  res_sts = Quote.update_quote( quote_id=quote_id, img_url=img_url )

  print(res_sts)

if __name__ == '__main__':
  main()
