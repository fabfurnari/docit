from docit import app
from flask import render_template
from docit.model import db, Snippet, Tag
from docit.aux import Pagination

log = app.logger

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    p = Pagination(per_page=10, current_page=page)
    
    sn = db.session.query(Snippet).all()
    tags = db.session.query(Tag).all()
    return render_template('index.html', snippets=sn, tags=tags, pagination=p)

