#!/usr/bin/env python
from docit import app, db
from docit.api import api
db.create_all()
app.run(debug=True)

