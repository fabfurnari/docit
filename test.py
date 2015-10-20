#!/usr/bin/env python
from docit import db
from docit.webapp import app
from docit.api import api
db.create_all()
app.run(debug=True)
