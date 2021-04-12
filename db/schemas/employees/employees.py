""" Employees table schema """


class EmployeesSchema:
    """CREATE TABLE IF NOT EXISTS employees \
        (employee_id INTEGER PRIMARY KEY NOT NULL, \
        first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, \
        home_address TEXT, mobile_number INTEGER, \
            country TEXT, state TEXT)
        """
    

