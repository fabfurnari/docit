from docit import app
from flask import render_template
from docit.model import db, Snippet, Tag

log = app.logger

@app.route('/')
def index():
    sn = db.session.query(Snippet).all()
    tags = db.session.query(Tag).all()
    return render_template('index.html', snippets=sn, tags=tags)

