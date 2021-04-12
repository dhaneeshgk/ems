''' Module for employees queries from database '''

from utils.wrappers import singleton
from db.db_utils import queries
from db.db_utils import utils
from db.config import DB_PATH

@singleton
class EmployeesQueries:
    __name__ = 'employees'
    columns = ['employee_id', 'first_name', 'last_name', 'email', \
        'home_address', 'mobile_number', 'country', 'state']
    
    filters = ['filter_operator']

    def get_employees(self, *columns, filter=None):
        '''
        Query handlers for fecting the employees information
        Paramters: 
            - list of columns
            - filter
                - any employee info
                - filter operator to fetch for all or any matches
        Return:
            - status - Boolean
            - employess information - List of Dict 
        '''

        source = queries.Source(self.__name__)

        # validate for query/filter params
        if filter:
            if self.validate_query(**filter):
                where = queries.Where(**filter)
            else:
                return False, "Invalid query param"
        else:
            where = ''

        columns = queries.Columns(*columns) if columns else queries.Columns()
        
        # form the query
        Query = str(queries.SelectQuery(source, columns, where))


        # establish connection to db and execute the 
        # query to employees records
        with utils.SqliteDB(DB_PATH) as connection:

            # get the cursor to execute query
            with utils.DBCursor(connection) as cursor:
                try:
                    employees = cursor.execute(Query).fetchall()
                except Exception as e:
                    return False , str(e)

        columns = columns.columns if columns.columns else self.columns
        employees_info = []
        for employee_info in employees:
            employees_info.append({column:value for column, value in zip(columns,employee_info)})

        return True, employees_info


    def create_employees(self, *employees):
        '''
        Query handlers for creating the employees information
        Paramters: 
            - list of employees records
        Return:
            - status
                - conatining successful and failed records
                  with error info
        '''
       
        source = queries.Source(self.__name__)
        status = {"success":[], "fail":[]}
        
        # connect to db
        with utils.SqliteDB(DB_PATH) as connection:
            for employee_detail in employees:
                if self.validate_request_params(**employee_detail):
                    values = queries.Values(**employee_detail)

                    #formation of query for record creation
                    iq = queries.InsertQuery(source, values)

                    # get the cursor to execute query
                    with utils.DBCursor(connection) as cursor:
                        try:
                            cursor.execute(str(iq)) 
                            status["success"].append({"record":employee_detail})  
                        except Exception as e:
                            status["fail"].append({'record':employee_detail, 'error': str(e)})
                else:
                    status["fail"].append({'record':employee_detail, 'error': "Invalid attributes in request body"})           
        return status

    def update_employees_info(self, *employees):
        '''
        Query handlers for updating the employees information
        Paramters: 
            - list of employees records to be updated
        Return:
            - status
                - conatining successful and failed records
                  with error info
        '''

        status = {"success":[], "fail":[]}

        source = queries.Source(self.__name__)

        # establish connection to db
        with utils.SqliteDB(DB_PATH) as connection:
            for employee_detail in employees:
                if self.validate_request_params(**employee_detail):
                    if "employee_id" in employee_detail:
                        set_values = queries.Set(**{key:employee_detail[key] for key in employee_detail if key!='employee_id'})
                        where = queries.Where(employee_id=str(employee_detail["employee_id"]))
                        
                        # formation of query
                        uq = queries.UpdateQuery(source.sources[0], set_values, where)
                        
                        # get the cursor to execute query
                        with utils.DBCursor(connection) as cursor:
                            try:
                                cursor.execute(str(uq))
                                status["success"].append({"record":employee_detail})  
                            except Exception as e:
                                status["fail"].append({'record':employee_detail, 'error': str(e)})
                    else:
                        status["fail"].append({'record':employee_detail, 'error': "Not provided required attribute to update"})
                else:
                    status["fail"].append({'record':employee_detail, 'error': "Invalid attributes in request body"}) 
        return status

    
    def delete_employees(self, **employees):
        '''
        Query handlers for deleting the employee information
        Paramters: 
            - employee_id
        Return:
            - status
                - conatining successful deletion
        '''
        source = queries.Source(self.__name__)

        # establish connection to db
        with utils.SqliteDB(DB_PATH) as connection:

            # validate for query
            if self.validate_request_params(**employees):

                # get the cursor to execute query
                with utils.DBCursor(connection) as cursor:
                    where = queries.Where(**employees)
                    dq = queries.DeleteQuery(source, where)
                    try:
                        cursor.execute(str(dq))
                    except Exception as e:
                        return False, {'error': str(e)}
            else:
                return False, {'error': "Invalid attributes in request body"}
        return True, {"message":"Deleted sucessfully"}


    def validate_query(self, **query):
        '''
        Validate the query params  with employees columns and
        other key params which are needed
        Paramters:
            - all query params from request
        Return:
            - Boolean - True or False
        '''

        all_query_params = self.columns
        all_query_params.extend(self.filters)
        if set(query.keys()).difference(set(all_query_params)):
            return False
        else:
            return True
    
    def validate_request_params(self, **attributes):
        '''
        Validate the request body params  with employees columns

        Paramters:
            - all request body params from request
        Return:
            - Boolean - True or False
        '''
        if set(attributes.keys()).difference(set(self.columns)):
            return False
        else:
            return True

