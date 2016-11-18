from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
import cgi
import os


def MakeHandler(grenouille_bot):
    class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
        
        def do_POST(self):
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={"REQUEST_METHOD": "POST"}
                )

                headerkey = 'X-Grenouille-Api-Key'
                if (not headerkey in self.headers):
                    return self.unauthorized()
                
                key, values = cgi.parse_header(self.headers[headerkey])
                
                if (key != grenouille_bot.grenouille_bot.config['DEFAULT']['grenouille_api_key']):
                    return self.unauthorized()
                    
                    
                for item in form.list:
                    if (item.name == "say"):
                        grenouille_bot.bot.send_msg(item.value)
                        
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        return
            except Exception as e:
                logging.info(e)


        def unauthorized(self):
            self.send_response(403)
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
            myhandler = MakeHandler(self)
            httpd = HTTPServer(server_address, myhandler)
            logging.info('webserver started on port ' + str(port))
            httpd.serve_forever()
        except Exception as e:
            logging.info(e)
        
