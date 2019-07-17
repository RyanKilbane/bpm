from sqlalchemy import create_engine
from sqlalchemy.engine import reflection

class Metadata:
    def __init__(self, test_env=False, table_name=None, db_name=None, schema=None):
        self.env = test_env
        self.table = table_name
        self.db_name = db_name
        self.schema = schema
        self.engine = None

    def make_engine(self):
        if self.env == True:
            self.engine = create_engine('sqlite:///:memory', echo=True)
        else:
            pass
    
    def get_table_data(self):
        inspect = reflection.Inspector.from_engine(self.engine)
        inspect.get_columns(self.table_name, self.schema)
