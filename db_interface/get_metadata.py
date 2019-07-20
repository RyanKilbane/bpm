from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import Session
from parse_config import config

class Metadata:
    def __init__(self, test_env=False, table_name=None, db_name=None):
        self.env = test_env
        self.table = table_name
        self.db_name = db_name
        self.engine = None

    def make_engine(self):
        if self.env == True:
            self.engine = create_engine('sqlite:///bpm_test', echo=True)
        else:
            pass
    
    def get_table_data(self):
        inspect = reflection.Inspector.from_engine(self.engine)
        return inspect.get_columns(self.table)
