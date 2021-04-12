from flask_restful import Api
from utils.wrappers import singleton
from resources.api_handlers import url_entries

@singleton
class EMS_APIs:
    def __init__(self, APP = None ):
        self.api = Api(APP)

    def initialize_resources(self):
        for url,handler in url_entries.items():
            self.api.add_resource(handler, url)