
''' Module to host swagger config JSON 
    for swagger portal '''

from flask_restful import Resource
import json

from swagger.config import SWAGGER_JSON_PATH


class Swagger(Resource):

    def get(self):
        with open(SWAGGER_JSON_PATH, "r") as swagger_json:
            content = json.loads(swagger_json.read())
        return content
    
