#!/usr/bin/env python
from docit import db
from docit.webapp import app
from docit.api import api

import logging
from logging.handlers import RotatingFileHandler

app.config.from_object('docit.config.Development')

app.logger.setLevel(app.config['LOG_LEVEL'])
handler = RotatingFileHandler(app.config['LOG_NAME'], maxBytes=10000, backupCount=1)
handler.setFormatter(app.config['LOG_FORMAT'])
app.logger.addHandler(handler)

db.init_app(app)
db.create_all()

app.run(debug=True)

