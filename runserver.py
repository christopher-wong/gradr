# -*- coding: utf-8 -*-
# !/usr/bin/python

import os
from application import app

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 443))
    host = '0.0.0.0'
    app.jinja_env.cache = {}

    app.run(host=host,
            port=port,
            debug=True,
            threaded=True)
