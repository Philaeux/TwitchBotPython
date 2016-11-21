from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import logging
import cgi
import os


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    """Handler used by the web server to manage requests.
    The handler expects 2 attributes from the self.server object

    secret - The API header secret
    grenouille_irc_bot - a link to the `GrenouilleIrcBot` object to send messages
    """

    def do_POST(self):
        """Manage a POST request done on the webserver.
        """
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST"}
            )

            header_key = 'X-Grenouille-Api-Key'
            if header_key not in self.headers:
                return self.unauthorized()

            key, values = cgi.parse_header(self.headers[header_key])

            if key != self.server.secret:
                return self.unauthorized()

            for item in form.list:
                if item.name == "say":
                    self.server.grenouille_irc_bot.send_msg(item.value)

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
        except Exception as e:
            logging.info(e)

    def unauthorized(self):
        """Handler of unauthorized POST calls.
        """
        self.send_response(403)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return


class GrenouilleHttpServer(Thread):
    """Thread responsible for managing http requests.

    Attributes
        port - server port
        server_adress - full server address (ip+port)
        httpd - HTTP server instance
    """

    def __init__(self, grenouille_bot):
        """Create a HTTP server to manage commands.

        :param grenouille_bot: Master class linked to the web server
        :type grenouille_bot: `GrenouilleBot`
        """
        Thread.__init__(self)

        self.port = int(os.environ['WEBSERVER_PORT'])
        self.server_address = ('127.0.0.1', self.port)
        self.httpd = HTTPServer(self.server_address, HTTPServer_RequestHandler)
        self.httpd.grenouille_irc_bot = grenouille_bot.grenouille_irc_bot
        self.httpd.secret = grenouille_bot.config['DEFAULT']['grenouille_api_key']

    def run(self):
        """Start the thread accepting the external web requests
        """
        try :
            logging.info('webserver started on port ' + str(self.port))
            self.httpd.serve_forever()
        except Exception as e:
            logging.info(e)
