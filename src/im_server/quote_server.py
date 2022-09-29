
import logging
import socketserver

from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Any,Tuple
from bson.objectid import ObjectId

from definitions import HOST, PORT
from im_server import req_handler
from result import Result, Ok, Err, Some


_logger = logging.getLogger(__name__)


class _QuoteServerHandler ( SimpleHTTPRequestHandler ):


    def do_GET( self ):

        def is_mongo_id():
            oid = self.path.strip('/')
            try:
                ObjectId(oid)
                return True
            except Exception:
                return False

        if self.path == '/help':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            help_json_str: str = req_handler.get_help_json().unwrap_or(r"{}")
            self.wfile.write(bytes(help_json_str, 'utf-8'))

        elif is_mongo_id():
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            help_json_str: str = r'{"foo": "bar"}'
            self.wfile.write(bytes(help_json_str, 'utf-8'))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>404</title></head>", "utf-8"))
            self.wfile.write(bytes('<body style="box-sizing: border-box; color: #dedede; background-color: #333;">', "utf-8"))
            self.wfile.write(bytes('<h1 style="text-align: center; font-size: 128px; padding: 64px;">404</h1>', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))



    def do_POST( self ):


        print(f'{self.path=}')
        tt = self.path.strip('/')
        print('path', tt)
        

        match req_handler.create_quote_img( self ):

            case Ok( response_json_str ):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(response_json_str, 'utf-8'))

            case Err( err ):
                _logger.error(err, exc_info=True )
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                fata_err_str = '{"err":"General error 500","message":"Could not create quote image","details":['+err+']}'
                self.wfile.write(bytes(fata_err_str, 'utf-8'))


    def log_message(self, format: str, *args: Any) -> None:
        
        arg: str = ''

        try: arg = str(args)
        except Exception: pass

        req_log: str = f'{self.address_string()} - {self.log_date_time_string()} - {arg}'
        _logger.info( req_log )
        

def init():

    server_addr: Tuple[str, int] = ( HOST, PORT )
    quote_server = HTTPServer( server_addr, _QuoteServerHandler )

    print(f'Starting: {HOST}:{PORT}')
    try:
        #solution for `OSError: [Errno 98] Address already in use`
        socketserver.TCPServer.allow_reuse_address = True  

        quote_server.serve_forever()

    except KeyboardInterrupt:
        print('Stoped by "Ctrl+C"')

    finally:
        quote_server.server_close()
