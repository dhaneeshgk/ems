from db.db_utils.utils import SqliteDB, DBCursor
from db.schemas.employees import employees

schemas = [employees.EmployeesSchema]


def create_all():
    """create table using schema if table not exists"""

    with SqliteDB('./db/.store/ems.db') as connection:
        with DBCursor(connection) as cursor:
            for schema in schemas:
                cursor.execute(schema.__doc__)

