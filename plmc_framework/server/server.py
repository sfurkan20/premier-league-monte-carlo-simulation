from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse

from plmc_framework.settings import settings
from plmc_project.models.team import TeamModel

class PLMCRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=settings.PUBLIC_HTML_ABSOLUTE_PATH, **kwargs)
        
    def do_GET(self) -> None:
        url = urlparse(self.path)
        if url.path == "/get_teams":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            teamModels = [model.__dict__ for model in TeamModel.getAll()]
            self.wfile.write(json.dumps(teamModels).encode('ascii'))
        else:
            super().do_GET()

    """def do_GET(self) -> None:
        print(self.path)
        url = urlparse(self.path)
        if url.path in plmc_framework.server.urls.urls.keys():
            self.send_response(200)
            mimetype, _ = mimetypes.guess_type(self.path)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(plmc_framework.server.urls.urls[url.path]().encode('ascii'))
        else:
            super().do_GET(self)
"""

class PLMC_HTTPServer(HTTPServer):
    def __init__(self):
        super().__init__((settings.HOST_NAME, settings.PORT), PLMCRequestHandler, True)