from datetime import datetime
import logging
import os

from qt_server.quote_server import init_quote_server
from definitions import LOGS_DIR
from imgen.imgen import ImGen
from models.im_request import ImRequest
from result import Result, Ok, Err

def _load_logger() -> None:

    timestamp = str( datetime.now() )
    date_str = timestamp[0:10]
    filename = f"{date_str}-quote-server.log"
    output_dir =  LOGS_DIR
    file_path = os.path.join( output_dir, filename )
    logging.basicConfig(
        filename = file_path,
        level = logging.DEBUG,
        format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode = 'a+'
    )

def main():
    im_req = ImRequest()
    #print(im_req)
    dd = {
        "quote_id": "63139372217ba7e20813b9b3",
        "author": {
            "name": "Chiquinha",
            #"img_name": "chiquinha"
        },
        "quote_text": 'RGB',
        #"quote_text": "Minhas tias não me deixavam fazer nada, eu queria brincar de fogueirinha com os móveis novos da minha tia, não. Eu queria fazer uma tenda de campanha no jardim, com a cortina da sala, não. Eu queria laçar a televisão com uma corda, não. Acredita que não me deixaram fazer um dominó com as teclas do piano? E com o trabalho que eu tive pra tirar as teclas do piano…",
        #"width": 800,
        # "height": 600
    }

    _load_logger()
    match ImGen( im_req ).gen_quote():
        case Ok( img):
            print( 'PASSOU')
            img.show()
        case Err( err ):
            print(err)
    #imgen.create_quote_img( dd )

if __name__ == '__main__':
    main()
