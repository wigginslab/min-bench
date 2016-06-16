# Login scripts modified from https://gist.github.com/guillaumevincent/4771570
import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, "public/static")
GAUTH_CLIENT_ID = "692990912471-c60j5rf40at2j1724smps1nfcvs7s96e.apps.googleusercontent.com"
GAUTH_CLIENT_SECRET = "nfNkd4LFas9FLPoOnQgQ6f5A"
TEMPLATE_PATH = os.path.join(DIRNAME, "public/static")
PORT = 3036

import logging
import sys
#log linked to the standard error stream
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)-8s - %(message)s",
                    datefmt="%d/%m/%Y %Hh%Mm%Ss")
console = logging.StreamHandler(sys.stderr)

COOKIE_SECRET = "a6Ca7pnQQfaNUeES9RjAzBEBlDbznEsamds7rHFy0Ng="

ANGEL_LIST_ID = "877b8e7f89b67117030725c93f7787eb2e2d240222916ae1"
ANGEL_LIST_SECRET = "fac08c4a43771aa1a8b57969c32d6a8bbb4b380cccf09562"
