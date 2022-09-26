from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import logging
import socketserver
from time import sleep
from typing import Any, Tuple

from definitions import HOST, PORT



class __QuoteServerHandler ( SimpleHTTPRequestHandler ):


    def do_GET( self ):

        # self.send_error(404)
        # self.send_response(404)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()

        if ( self.path == '/sleep'):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            print(self.path)
            sleep(5)
            self.wfile.write(bytes("<html><head><title>405</title></head>", "utf-8"))
            self.wfile.write(bytes('<body style="box-sizing: border-box; color: #dedede; background-color: #333;">', "utf-8"))
            self.wfile.write(bytes('<h1 style="text-align: center; font-size: 128px; padding: 64px;">404</h1>', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>404</title></head>", "utf-8"))
            self.wfile.write(bytes('<body style="box-sizing: border-box; color: #dedede; background-color: #333;">', "utf-8"))
            self.wfile.write(bytes('<h1 style="text-align: center; font-size: 128px; padding: 64px;">404</h1>', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))



    def do_POST( self ):

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        #### MEU HANDLER ####

        self.send_response(200)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
      

        # data = json.loads(self.data_string)
        
        # self.wfile.write(bytes(json.dumps(data, ensure_ascii=False), 'utf-8'))
        


    def log_message(self, format: str, *args: Any) -> None:
        
        arg: str = ''

        try: arg = str(args)
        except Exception: pass

        req_log: str = f'{self.address_string()} - {self.log_date_time_string()} - {arg}'
        logging.info( req_log )
        


def init_quote_server():

    server_addr: Tuple[str, int] = ( HOST, PORT )
    quote_server = HTTPServer( server_addr, __QuoteServerHandler )

    print(f'Starting: {HOST}:{PORT}')
    try:
        #solution for `OSError: [Errno 98] Address already in use`
        socketserver.TCPServer.allow_reuse_address = True  

        quote_server.serve_forever()

    except KeyboardInterrupt:
        print('Stoped by "Ctrl+C"')

    finally:
        quote_server.server_close()