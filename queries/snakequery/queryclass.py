import time

class SnakeQueryObj:
    def __init__(self):
        # SnakeQuery Information
        self.name = ''
        self.number = ''
        self.description = ''
        self.author = ''
        self.version = ''

        # Database Connection Information
        self.server = ''
        self.instance = ''
        self.port = ''

        # Query Specific Details
        self.database = ''
        self.schema = ''
        self.table = ''
        self.columns = ['']

        # Runtime Modifiers/
        self.mod_columns = ''
        self.mod_filter = ''
        self.mod_top = ''


    def plugin_check(self, queryid):
        if queryid == self.number:
            return True
        else:
            return False

    def plugin_load(self, col, fil, top):
        if not col == '':
            try:
                cols = col.split(",")
                self.columns = cols
            except:
                cols = ['']
        self.mod_filter = fil
        self.mod_top = top

    def _get_server_string(self):
        if self.instance == '':
            return self.server# + ":" + self.port
        else:
            return self.server + "\\" + self.instance# + ":" + self.port

    def _get_table_string(self):
        if self.schema == '':
            return self.database + '.[' + self.table + ']'
        else:
            return  self.database + '.' + self.schema + '.[' + self.table  + ']'

    def _get_columns_string(self):
        tmpstr = ''
        for entry in self.columns:
            tmpstr = tmpstr + ', [' + entry +']'
        return tmpstr.lstrip(", ")

    def get_query_string(self):
        return 'SELECT' + ' ' + self.mod_top + ' ' + self._get_columns_string() + ' ' + 'FROM' + ' ' + self._get_table_string() + ' ' + self.mod_filter

    def _print_query_string(self):
        print(self._get_query_string(self))

    def get_filename(self):
        file_name = self.server + "_" + self.database + "_" + self.table + "_" + time.time().__str__()
        return file_name

    def get_conn_string(self, input_auth="Trusted_Connection=yes"):
        self.conn_string = "Driver={SQL Server};"
        self.conn_string += "Server=" + self._get_server_string() + ";"
        self.conn_string += "Database=" + self.database + ";"
        self.conn_string += input_auth + ";"
        return self.conn_string

    def info(self):
        print('{0:15} {1}'.format("ID:", self.number))
        print('{0:15} {1}'.format("Name:", self.name))
        #print('{0:15} {1}'.format("Author:", self.author))
        #print('{0:15} {1}'.format("Version:", self.version))
        #print('{0:15} {1}'.format("Description:", self.description))

        print('{0:15} {1}'.format("Server Info:", self._get_server_string()))
        print('{0:15} {1}'.format("Table Info:", self._get_table_string()))
        print('{0:15} {1}'.format("SQL String:", self.get_conn_string()))
        print('{0:15} {1}'.format("Columns:", self._get_columns_string()))

    def get_queryid(self):
        return self.number

    def get_columns(self):
        return self.columns
