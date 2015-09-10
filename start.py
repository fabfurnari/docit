#!/usr/bin/env python
from docit import app, db
from docit.api import api
app.run(debug=True)
db.create_all()
