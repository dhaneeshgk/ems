"""
Module to map to url entries to resource/handler
"""
from resources.handlers.employees.employees import Employees
from resources.handlers.swagger.swagger import Swagger

### url entry mappings to resource/handler
url_entries = {
    "/employees":Employees,
    "/swagger":Swagger
}
