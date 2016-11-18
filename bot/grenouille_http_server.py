from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
import cgi
import os


def MakeHandler(bot):
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
    return testHTTPServer_RequestHandler

class GrenouilleHttpServer:

    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot
        
    def start(self):
        try :
            self.bot = self.grenouille_bot.grenouille_irc_bot
            threading.Thread(target=self.runserver).start()
        except Exception as e:
            logging.info(e)

            
    def runserver(self):
        try :
            port = int(os.environ['WEBSERVER_PORT'])
            server_address = ('127.0.0.1', port)
            myhandler = MakeHandler(self.bot)
            httpd = HTTPServer(server_address, myhandler)
            logging.info('webserver started on port ' + str(port))
            httpd.serve_forever()
        except Exception as e:
            logging.info(e)
        
