import types

from docit import api, app
from docit.model import db, Snippet, Tag
from flask_restful import Resource, reqparse, abort, fields, marshal_with

log = app.logger

parser = reqparse.RequestParser()
parser.add_argument('value', required=True, help='Snippet content')
parser.add_argument('tags', action='append', required=False, help='List of space separated tags')
parser.add_argument('user', help='The username')
parser.add_argument('path', help='Current client\'s path')
parser.add_argument('hostname', help='Client\'s hostname')

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

def api_route(self, *args, **kwargs):
    '''
    To route api's endpoint like flask standard ones.
    From: http://flask.pocoo.org/snippets/129/
    '''
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper
api.route = types.MethodType(api_route, api)

def abort_if_not_exists(snippet_id):
    '''
    Helper function
    '''
    sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if not sn:
        m = "Snippet %s does not exists" % snippet_id
        log.error(m)
        abort(404, message=m)

def create_snippet(snippet_id, args):
    '''
    Actually create the snippet
    '''
    tag_list = []
    
    if not args['tags']:
        log.debug('No tags, applying the default \'notag\' tag')
        args['tags'] = ['notag']
        
    for tag in args['tags']:
        t = Tag.query.filter(Tag.text.like(tag)).first()
        if not t:
            t = Tag(text=tag.lower())
            log.info('New tag found %s, adding to our database' % t)
            db.session.add(t)
        tag_list.append(t)

    sn = Snippet(snippet_id,
                 value=args['value'],
                 tags=tag_list,
                 user=args['user'],
                 path=args['path'],
                 hostname=args['hostname'])
    db.session.add(sn)
    log.info('Adding snippet %s ' % sn)
    db.session.commit()
    return sn

@api.route('/api','/api/')
class SnippetListResource(Resource):
    '''
    Get full list of snippets or create a new snippet
    '''
    @marshal_with(snippet_fields)
    def get(self):
        '''
        Get all snippets
        '''
        log.debug('Getting snippet list')
        p = reqparse.RequestParser()
        p.add_argument('sorting', default='id')
        p.add_argument('reverse', default=False)
        p.add_argument('paginate', type=int)
        p.add_argument('offset', type=int, default=1)
        p.add_argument('filter')
        a = p.parse_args()
        log.debug('List of args: %s' % a)

        column_sort = getattr(Snippet, a['sorting'])
        query_filter = Snippet.value.like("%{}%".format(a['filter']))
        
        if not a['filter']:
            q = Snippet.query
        else:
            q = Snippet.query.filter(query_filter)

        if a['reverse']:
            q = q.order_by(column_sort.desc())
        else:
            q = q.order_by(column_sort.asc())

        if a['paginate']:
            q = q.paginate(a['offset'], a['paginate'], False).items
        else:
            q = q.all()

        log.debug('Returning snippets: %s' % q)
        return q, 200

    @marshal_with(snippet_fields)
    def post(self):
        '''
        Create snippet
        '''
        log.debug('Creating new snippet')
        args = parser.parse_args()
        log.debug('Args: %s' % args)
        id_list = [x for x, in db.session.query(Snippet.id).all()]
        if id_list:
            snippet_id = int(max(id_list) + 1)
        else:
            snippet_id = 0
            log.info('Creating snippet in empty bucket')
        sn = create_snippet(snippet_id, args)
        log.debug('Snippet %s created' % sn)
        return sn, 201

    def delete(self):
        '''
        Deletes all snippets
        TODO: use confirmation mechanisms
        '''
        log.warning('Deleting all snippets!')
        deleted_rows = db.session.query(Snippet).delete()
        db.session.commit()
        return {'value': 'All {} snippets deleted'.format(deleted_rows)}, 200        

@api.route('/api/<int:snippet_id>')
class SnippetResource(Resource):
    @marshal_with(snippet_fields)
    def get(self, snippet_id):
        '''
        Get single snippet
        '''
        log.debug('Getting single snippet')
        abort_if_not_exists(snippet_id)
        s = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        log.debug('Snippet %s ' % s)
        return s, 200

    @marshal_with(snippet_fields)
    def put(self, snippet_id):
        '''
        Update snippet
        '''
        log.debug('Updating snippet')
        args = parser.parse_args()
        sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        log.info('Updating snippet %s' % sn)
        sn.value = args['value']
        db.session.add(sn)
        db.session.commit()
        log.debug('Updated snuppet %s' % sn)
        return sn, 201

    @marshal_with(snippet_fields)
    def delete(self, snippet_id):
        '''
        Delete snippet
        '''
        log.debug('Deleting snippet')
        abort_if_not_exists(snippet_id)
        sn = db.session.query(Snippet).filter(Snippet.id == snippet_id).first()
        log.warning('Deleting snippet %s' % sn)
        db.session.delete(sn)
        db.session.commit()
        log.debug('Snippet %s deleted' % sn)
        return {}, 204

    def post(self, snippet_id):
        log.error('Method POST not allowed here')
        abort(405, message="Method not allowed")

@api.route('/api/tags','/api/tags/','/api/tags/<tag_name>')
class TagListResource(Resource):
    @marshal_with(tag_fields)
    def get(self, tag_name=None):
        log.debug('Getting tag list')
        if not tag_name:
            tag_list = db.session.query(Tag).all()
        else:
            tag_list = db.session.query(Tag).filter(Tag.text.startswith(tag_name)).all()
        log.debug('Tag list: %s' % tag_list)
        return tag_list
