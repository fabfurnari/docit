from docit import db
import datetime

class Snippet(db.Model):
    __tablename__ = 'Snippet'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String())
    tags = db.Column(db.String())
    user = db.Column(db.String())
    path = db.Column(db.String())
    hostname = db.Column(db.String())
    date_updated = db.Column(db.DateTime,
                             default=datetime.datetime.now(),
                             onupdate=datetime.datetime.now())
    
    def __init__(self,
                 snippet_id, data, tags,
                 user, path, hostname):
        self.id = snippet_id
        self.data = data
        self.tags = tags
        self.user = user
        self.path = path
        self.hostname = hostname
        

    def __repr__(self):
        return '<Snippet %r>' % self.id
