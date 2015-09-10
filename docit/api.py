from docit import api
from flask_restful import Resource, reqparse, abort

parser = reqparse.RequestParser()
parser.add_argument('snippet')

snippets = {}

class SnippetList(Resource):
    def get(self):
        return snippets

class Snippet(Resource):
    def get(self, snippet_id):
        return snippets[snippet_id]
    
    def put(self, snippet_id):
        args = parser.parse_args()
        line = {'snippet': args['snippet']}
        snippets[snippet_id] = line
        return line, 201

api.add_resource(SnippetList, '/api')
api.add_resource(Snippet, '/api/<snippet_id>')
