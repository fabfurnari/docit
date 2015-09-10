from docit import db

class DBSnippet(db.Model):
    __tablename__ = 'Snippet'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String())
    tags = db.Column(db.String())
    
    def __init__(self, snippet_id, data, tags):
        self.id = snippet_id
        self.data = data
        self.tags = tags

    def __repr__(self):
        return '<Snippet %r>' % self.id
