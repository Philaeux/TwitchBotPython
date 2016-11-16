from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
import cgi



class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"}
        )
            
        for item in form.list:
            if (item.name == "say"):
                bot.send_msg(item.value)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

class GrenouilleHttpServer:
    
    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot
        
    def start(self, grenouille_irc_bot):
        global bot
        bot = grenouille_irc_bot

        try:
            self.server = threading.Timer(11, self.runserver).start()
        except Exception:
            logging.info(Exception)

    def runserver(self):
        port = 8083
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        logging.info('webserver started on port ' + str(port))
        httpd.serve_forever()

        
