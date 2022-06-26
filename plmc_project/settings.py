import os

class settings:
    DB_ABSOLUTE_PATH = os.path.join(__file__, "..", "..", "db", "db.sqlite")

    PUBLIC_HTML_ABSOLUTE_PATH = os.path.join(__file__, "..", "..", "public_html")

    HOST_NAME = '127.0.0.1'
    PORT = 8080