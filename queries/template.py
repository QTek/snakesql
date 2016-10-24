from snakequery.queryclass import SnakeQueryObj

class SnakeQuery(SnakeQueryObj):
    def __init__(self):
        # SnakeQuery Information
        self.name = 'Template Query'
        self.number = '0'
        self.description = 'A template query file'
        self.author = 'Name'
        self.version = '1.0'

        # Database Connection Information
        self.server = 'YOUR_SERVER'
        self.instance = 'YOUR_INSTANCE'

        # Query Specific Details
        self.database = 'YOUR_DB'
        self.schema = 'YOUR_SCHEMA'
        self.table = 'YOUR_TABLE'
        self.columns = ['COLUMN_1',
                        'COLUMN_2',
                        'COLUMN_3',
                        'COLUMN_4']




