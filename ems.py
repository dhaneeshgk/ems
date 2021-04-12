from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
import logging

from resources.ems_apis import EMS_APIs
from db import schemas
from swagger import config as swagger_config

import config


app = Flask(__name__)

## intialize the resource
EMS_APIs(APP=app).initialize_resources()

## basic log setup
logging.basicConfig(filename=config.LOG_PATH, level=logging.DEBUG, \
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


## swagger config

swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_config.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    swagger_config.API_URL,
    config={  # Swagger UI config overrides
        'app_name': "ems"
    })

if __name__=="__main__":
    schemas.create_all()
    app.register_blueprint(swaggerui_blueprint)
    app.run(debug=True)
    