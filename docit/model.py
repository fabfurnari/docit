from docit import db
import datetime

tagmap = db.Table('tagmap', db.Model.metadata,
                  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                  db.Column('snippet_id', db.Integer, db.ForeignKey('snippet.id'))
         )

class Snippet(db.Model):
    __tablename__ = 'snippet'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String())
    tags = db.relationship('Tag',
                           secondary=tagmap,
                           backref='snippets')
    user = db.Column(db.String())
    path = db.Column(db.String())
    hostname = db.Column(db.String())
    date_updated = db.Column(db.DateTime,
                             default=datetime.datetime.now(),
                             onupdate=datetime.datetime.now())
    
    def __init__(self,
                 snippet_id, value, tags,
                 user, path, hostname):
        self.id = snippet_id
        self.value = value
        self.tags = tags
        self.user = user
        self.path = path
        self.hostname = hostname
        

    def __repr__(self):
        return '<Snippet %r>' % self.id

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(80), unique = True)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Tag %r>' % self.text

    
