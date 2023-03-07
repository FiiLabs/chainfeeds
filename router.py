from flask_restful import Resource
from flask_restful_swagger_2 import swagger

class HelloWorld(Resource):
    @swagger.doc({
        'tags': ['helloworld'],
        'description': 'Returns Hello world',
        'responses': {
            '200': {
                'description': 'Hello world message'
            }
        }
    })
    def get(self):
        return {'hello': 'world'}