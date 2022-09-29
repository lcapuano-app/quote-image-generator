import logging
import os
import pyfiglet
from colorama import Fore, Style
from datetime import datetime
from dotenv import load_dotenv

from imserver import im_server
from definitions import LOGS_DIR, ROOT_DIR, WORKSPACE_DIR

def _dot_env():
    dotenv_root_path = os.path.join(ROOT_DIR, '.env')
    dotenv_ws_path = os.path.join(WORKSPACE_DIR, '.env')

    if os.path.exists( dotenv_root_path ):
        load_dotenv(dotenv_root_path)
    elif os.path.exists( dotenv_ws_path ):
        load_dotenv(dotenv_ws_path)
    else:
        raise FileExistsError(f'{Fore.LIGHTRED_EX}Could not found .env file.{Style.RESET_ALL}')

def _print_wellcome():
    print(Fore.GREEN)
    print(pyfiglet.figlet_format( "imgen" ))
    print(Style.RESET_ALL)

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
    _print_wellcome()
    _dot_env()
    _load_logger()
    im_server.init()

if __name__ == '__main__':
    main()
