import logging
import os.path
import datetime

from typing import Any

class ErrorLog():

  def log( err: Any ) -> None:
    timestamp = str( datetime.datetime.now() )
    date_str = timestamp[0:10]

    file_name = date_str + ' errors.txt'
    file_path = os.path.join( 'zz_logs', file_name )

    with open( file=file_path, mode='a+' ) as file:
      err_str = timestamp + ' |8==D>: '
      err_str += str( err ) + '\n'

      file.write( err_str )
      file.close()
