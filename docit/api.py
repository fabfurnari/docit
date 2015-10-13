from docit import api
from docit.model import db, Snippet, Tag
from flask_restful import Resource, reqparse, abort, fields, marshal_with

parser = reqparse.RequestParser()
parser.add_argument('value',
                    required=True,
                    help='Snippet content')
parser.add_argument('tags',
                    action='append',
                    required=False,
                    help='List of space separated tags')
parser.add_argument('user',
                    help='The username')
parser.add_argument('path',
                    help='Current client\'s path')
parser.add_argument('hostname',
                    help='Client\'s hostname')

snippet_fields = {
    'id': fields.Integer,
    'value': fields.String,
    'tags': fields.List(fields.String),
    'user': fields.String,
    'path': fields.String,
    'hostname': fields.String,
    'date_updated': fields.DateTime,
}

tag_fields = {
    'id': fields.Integer,
    'text': fields.String,
}

def abort_if_not_exists(snippet_id):
    sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if not sn:
        abort(404, message="Snippet %s does not exists" % snippet_id)

def create_snippet(snippet_id, args):
    tag_list = []
    if not args['tags']:
        args['tags'] = ['notag']
    for tag in args['tags']:
        t = Tag.query.filter(Tag.text.like(tag)).first()
        if not t:
            t = Tag(text=tag.lower())
            db.session.add(t)
        tag_list.append(t)

    print args['value']
            
    sn = Snippet(snippet_id,
                 value=args['value'],
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
        sn.value = args['value']
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
    
class TagListResource(Resource):
    @marshal_with(tag_fields)
    def get(self, tag_name=None):
        if not tag_name:
            tag_list = db.session.query(Tag).all()
        else:
            tag_list = db.session.query(Tag).filter(Tag.text.startswith(tag_name)).all()
        return tag_list

api.add_resource(SnippetListResource, '/api', '/api/')
api.add_resource(SnippetResource, '/api/<int:snippet_id>')
api.add_resource(TagListResource,
                 '/api/tags',
                 '/api/tags/',
                 '/api/tags/<tag_name>')

