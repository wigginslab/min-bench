# Login scripts modified from https://gist.github.com/guillaumevincent/4771570
import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, "static")
GAUTH_CLIENT_ID = "692990912471-c60j5rf40at2j1724smps1nfcvs7s96e.apps.googleusercontent.com"
GAUTH_CLIENT_SECRET = "nfNkd4LFas9FLPoOnQgQ6f5A"
TEMPLATE_PATH = os.path.join(DIRNAME, "templates")
PORT = 3036
HOST = "localhost"

import logging
import sys
#log linked to the standard error stream
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)-8s - %(message)s",
                    datefmt="%d/%m/%Y %Hh%Mm%Ss")
console = logging.StreamHandler(sys.stderr)

COOKIE_SECRET = "a6Ca7pnQQfaNUeES9RjAzBEBlDbznEsamds7rHFy0Ng="
