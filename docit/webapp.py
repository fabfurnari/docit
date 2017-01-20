from docit import app
#from docit.model import db, Snippet, Tag

#log = app.logger

@app.route('/')
def index():
    sn = db.session.query(Snippet).all()
    tags = db.session.query(Tag).all()
    return render_template('index.html', snippets=sn, tags=tags)

if __name__ == '__main__':
    app.run(debug=True)
