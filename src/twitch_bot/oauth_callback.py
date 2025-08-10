import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from PySide6.QtCore import QThread, Signal


class OAuthHandler(BaseHTTPRequestHandler):
    """Serveur web minimal."""

    oauth_code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            OAuthHandler.oauth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentification terminee. Vous pouvez fermer cette page.")
        else:
            self.send_response(400)
            self.end_headers()


class OauthCallback(QThread):
    """Thread QT qui écoute le retour de l'OAuth."""

    oauth_code = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        port = 9555
        server = HTTPServer(("localhost", port), OAuthHandler)

        # Attend une seule requête
        server.handle_request()
        self.oauth_code.emit(OAuthHandler.oauth_code)
