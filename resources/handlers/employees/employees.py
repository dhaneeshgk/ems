"""
Employees module to provide resource for 
fecthing 
    - List of employees
    - Update bulk employees info
    - delete employees
    - create bulk employees
"""

from flask_restful import Resource
from flask_restful import request 
import json

from db.schemas.employees.queries import queries

class Employees(Resource):
    
    def get(self):
        ''' 
            GET HTTP Verb Resource to fetch employees infromation from EMS System
            Return : 
                - JSON object containing all employees info
                - JSON object conatining employees infos based on employees info provided
                    - all info match
                    - any info match
        '''

        ## query to database fetch employees info
        status, employees = queries.EmployeesQueries().get_employees(filter=request.args) \
            if request.args else queries.EmployeesQueries().get_employees()
        
        if status:
            return {"data":{"employees":employees, "total_no_employees": len(employees)}}, 200
        else:
            return {"error": employees}, 404

    def post(self):
        '''
            POST HTTP Verb Resource to create employees records in EMS system
            Return : 
                - JSON Object containig
                    - succesfull list of employees records created
                    - failure list of employees records which were not created with error message
                    - count of success, failure and total employee records created
        '''

        ## fetch the request body
        json_data = request.get_json()

        if json_data:
            if "employees_info" in request.get_json():

                # query for the creation of employees record
                status = queries.EmployeesQueries().create_employees(*json_data["employees_info"])
            
                # status code assignment based on number of records success updation
                status_code = 201 if len(json_data["employees_info"])==len(status["success"]) \
                    else  409 if len(json_data["employees_info"])==len(status["fail"]) else 207

                return {'status':status,'metadata':{'success':len(status["success"]),\
                    'fail':len(status["fail"]), 'total':len(json_data["employees_info"])}}, status_code
            else:
                return {"message":"No body content provided"}, 400
        else:
            return {"message":"No body content provided"}, 400

    def put(self):
        '''
            POST HTTP Verb Resource to create employees records in EMS system
            Return : 
                - JSON Object containig
                    - succesfull list of employees records updated
                    - failure list of employees records which were not updated with error message
                    - count of success, failure and total of employee records updated
        '''

        # fetch the request body
        json_data = request.get_json()

        if json_data:
            if "employees_info" in request.get_json():
                
                # query for the updation of employees record
                status = queries.EmployeesQueries().update_employees_info(*json_data["employees_info"])

                # status code assignment based on number of records success updation
                status_code = 201 if len(json_data["employees_info"])==len(status["success"]) \
                    else  409 if len(json_data["employees_info"])==len(status["fail"]) else 207
                    
                return {'status':status,'metadata':{'success':len(status["success"]),\
                    'fail':len(status["fail"]), 'total':len(json_data["employees_info"])}}, status_code
                
            else:
                return {"message":"No body content provided"}, 400
        else:
            return {"message":"No body content provided"}, 400

    def delete(self):
        '''
            DELETE HTTP Verb Resource to create employees records in EMS system
            Return : 
                - JSON Object containig message with successfull deletion of employee record
        '''
        status, employees = queries.EmployeesQueries().delete_employees(**request.args)
        if status:
            return employees, 200
        else:
            return {'error': employees}, 404
