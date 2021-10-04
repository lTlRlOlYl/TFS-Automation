import pyodbc

class DBConn():
    refresh_data_query = r"execute dbo.sp_<omitted>"
    get_data_query = r"select * from dbo.<omitted>"
    write_to_db_query = r"insert into dbo.<omitted> (id) values (cast(? as int))"
    get_audit_query = r"select Code, Title from <omitted> where Code = ?"
    get_audit_back_query = r"select Code, Title from <omitted> where Code = ?"
    
    connection_string='''
            Driver={ODBC Driver 17 for SQL Server};
            Server=<omitted>;
            Database=<omitted>;
            Trusted_Connection=yes;'''

    def execute_sql(self, query, persist=False, results=False, param=None):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        if param:
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        if results:
            data = cursor.fetchall()
        if persist:
            conn.commit()
        cursor.close()
        del cursor
        conn.close()
        if results:
            if data:
                return data

    def refresh_data(self):
        self.execute_sql(query=self.refresh_data_query, persist=True, results=False)

    def get_data(self):
        return self.execute_sql(query=self.get_data_query, persist=False, results=True)

    def get_audit(self, param):
        return self.execute_sql(query=self.get_audit_query, persist=False, results=True, param=param)

    def get_audit_back(self, param):
        return self.execute_sql(query=self.get_audit_back_query, persist=False, results=True, param=param)

    def write_to_db(self, param):
        self.execute_sql(query=self.write_to_db_query, persist=True, results=False, param=param)

