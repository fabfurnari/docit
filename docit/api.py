from docit import api
from docit.model import db, Snippet, Tag
from flask_restful import Resource, reqparse, abort, fields, marshal_with

parser = reqparse.RequestParser()
parser.add_argument('data',
                    required=True,
                    help='Snippet content')
parser.add_argument('tags',
                    action='append',
                    help='List of space separated tags')
parser.add_argument('user',
                    help='The username')
parser.add_argument('path',
                    help='Current client\'s path')
parser.add_argument('hostname',
                    help='Client\'s hostname')

snippet_fields = {
    'id': fields.Integer,
    'data': fields.String,
    'tags': fields.List(fields.String),
    'user': fields.String,
    'path': fields.String,
    'hostname': fields.String,
    'date_updated': fields.DateTime,
}

def abort_if_not_exists(snippet_id):
    sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if not sn:
        abort(404, message="Snippet %s does not exists" % snippet_id)

def create_snippet(snippet_id, args):
    tag_list = []
    for tag in args['tags']:
        t = Tag.query.filter(Tag.name.like(tag)).first()
        if not t:
            t = Tag(name=tag.lower())
            db.session.add(t)
        tag_list.append(t)
            
    sn = Snippet(snippet_id,
                 data=args['data'],
                 tags=tag_list,
                 user=args['user'],
                 path=args['path'],
                 hostname=args['hostname'])
    db.session.add(sn)
    db.session.commit()
    return sn
 
class SnippetListResource(Resource):
    @marshal_with(snippet_fields)
    def get(self):
        l = db.session.query(Snippet).all()
        return l

    @marshal_with(snippet_fields)
    def post(self):
        '''
        Create snippet
        '''
        args = parser.parse_args()
        id_list = [x for x, in db.session.query(Snippet.id).all()]
        if id_list:
            snippet_id = int(max(id_list) + 1)
        else:
            snippet_id = 0
        sn = create_snippet(snippet_id, args)
        return sn, 201

class SnippetResource(Resource):
    @marshal_with(snippet_fields)
    def get(self, snippet_id):
        abort_if_not_exists(snippet_id)
        s = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        return s

    @marshal_with(snippet_fields)
    def put(self, snippet_id):
        '''
        Update snippet
        '''
        args = parser.parse_args()
        sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        sn.data = args['data']
        db.session.add(sn)
        db.session.commit()
        return sn, 201

    @marshal_with(snippet_fields)
    def delete(self, snippet_id):
        '''
        Delete snippet
        '''
        abort_if_not_exists(snippet_id)
        sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        db.session.delete(sn)
        db.session.commit()
        return {}, 204


api.add_resource(SnippetListResource, '/api')
api.add_resource(SnippetResource, '/api/<int:snippet_id>')
