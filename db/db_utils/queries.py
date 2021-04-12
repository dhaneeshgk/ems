''' Generic module to create fomratted strings 
    to query sqlite DB '''

class Source:
    def __init__(self, *sources):
        if type(sources)==tuple:
            self._sources = sources
        else:
            self._sources = (sources)

    @property
    def sources(self):
        return self._sources

    def __str__(self):
        return 'FROM '+', '.join(self._sources)

class Columns:
    def __init__(self, columns=None):
        self._columns = columns

    @property
    def columns(self):
        return self._columns

    def __str__(self):
        if self._columns:
            return ', '.join(self._columns)
        else:
            return '*'

class Where:
    def __init__(self, filter_operator=None, **column_values,):
        self.column_values = column_values
        if filter_operator and filter_operator.lower() in ['or', 'and']:
            self.filter_operator = filter_operator.upper()  
        else:
            raise Exception("Invalid filter operator")
    
    def __str__(self):
        where = "WHERE "
        operator = " "+self.filter_operator+" "
        column_value = []
        for column, value in self.column_values.items():
            column_value.append(column + " = '" +str(value)+"'")
        return where+ operator.join(column_value)

class Set:
    def __init__(self, **column_values):
        self.column_values = column_values
    
    def __str__(self):
        Set = "SET "
        column_value = []
        for column, value in self.column_values.items():
            column_value.append(column + "='" + value + "'" )
        return Set+', '.join(column_value)   

class Values:
    def __init__(self, **column_values):
        self.column_values = column_values
    
    def __str__(self):
        Values = " VALUES "
        columns = []
        values = []
        for column, value in self.column_values.items():
            columns.append(column)
            values.append('"'+value+'"')
        return '('+','.join(columns)+')'+Values+'('+','.join(values)+')'

class SelectQuery:
    def __init__(self, source, columns, where=None):
        self.query = "SELECT"
        self.source = source
        self.columns = columns
        self.where = where
        
    def __str__(self):
        return self.query+' '.join([str(self.columns), str(self.source),
                        '' if not self.where else str(self.where)])

class InsertQuery:
    def __init__(self, source, values, where=None):
        self.query = "INSERT INTO "
        self.source = source.sources[0]
        self.values = values
        self.where = where
        
    def __str__(self):
        return self.query+' '.join([str(self.source), str(self.values),
                        '' if not self.where else str(self.where)])    

class UpdateQuery:
    def __init__(self, source, set_col, where):
        self.query = "UPDATE "
        self.source = source
        self.set_col = set_col
        self.where = where

    def __str__(self):
        return self.query+' '.join([str(self.source), str(self.set_col),
                        '' if not self.where else str(self.where)])


class DeleteQuery:
    def __init__(self, source, where):
        self.query = "DELETE "
        self.source = source
        self.where = where

    def __str__(self):
        return self.query+' '.join([str(self.source),
                        '' if not self.where else str(self.where)])


if __name__=='__main__':
    # source = Source('Employees', 'Users')
    # where = Where(employee_id=2, last_name="hello")
    # columns = Columns()
    # sq = SelectQuery(source, columns, where)
    # print(sq)

    # source = Source('Employees')
    # values = Values(first_name='hey', last_name='hello')
    # iq = InsertQuery(source, values)
    # print(iq)

    # source = Source('employees')
    # set_values = Set(first_name='hey', last_name='hello')
    # where = Where(employee_id=1)
    # uq = UpdateQuery(source.sources[0], set_values, where)
    # print(uq)

    # source = Source('employees')
    # where = Where(employee_id=1)
    # dq = DeleteQuery(source, where)
    # print(dq)

    pass