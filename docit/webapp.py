from docit import app
from flask import render_template
from docit.model import db, Snippet, Tag

@app.route('/')
def index():
    sn = db.session.query(Snippet).all()
    return render_template('index.html', snippets=sn)

