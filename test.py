#!/usr/bin/env python
from docit import db
from docit.webapp import app
from docit.api import api

app.config.from_object('docit.config.Testing')

db.init_app(app)
db.create_all()

app.run(debug=True)
