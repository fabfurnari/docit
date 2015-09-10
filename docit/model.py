from useheadphones import db
    
class AudioFiles(db.Model):
    __tablename__ = 'AudioFiles'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=True)
    file_hash = db.Column(db.String(), unique=True)
    
    def __init__(self, path, file_hash):
        self.path = path
        self.file_hash = file_hash

    def __repr__(self):
        return '<AudioFile %r>' % self.path

class AudioEntry(db.Model):
    __tablename__ = 'AudioEntry'
    entry_id = db.Column(db.Integer, db.ForeignKey(AudioFiles.id), primary_key=True)
    file_type = db.Column(db.String(10))

    def __init__(self, entry_id, file_type):
        self.entry_id = entry_id
        self.file_type = file_type

    def __repr__(self):
        return '<AudioEntry %r>' % self.entry_id
    
