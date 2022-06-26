import sys
sys.path.append(f"{__file__}/../../")

from plmc_framework.server.server import PLMC_HTTPServer
import plmc_framework.settings
import plmc_framework.server.urls
from plmc_framework.helpers import get_attribute_names

import settings
import urls

def registerToFramework():
    """
        Bridges the local project files with the framework modules.
    """

    for key in get_attribute_names(settings.settings):
        setattr(plmc_framework.settings.settings, key, settings.settings.__dict__[key])

    plmc_framework.server.urls.urls = urls.urls

def main():
    registerToFramework()

    httpd = PLMC_HTTPServer()
    httpd.serve_forever(0.1)

if __name__ == '__main__':
    main()