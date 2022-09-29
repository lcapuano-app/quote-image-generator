import logging
import os

from datetime import datetime
from dotenv import load_dotenv

from im_server import quote_server
from definitions import LOGS_DIR, ROOT_DIR

dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

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
    _load_logger()
    quote_server.init()

if __name__ == '__main__':
    main()
