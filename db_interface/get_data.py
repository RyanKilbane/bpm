from sqlalchemy.orm import sessionmaker
from db_interface.get_metadata import Metadata
from sqlalchemy import exc
from exceptions.insert_error import InsertError

class GetData:
    def __init__(self, database, table, orm_class, test_env):
        engine = Metadata(test_env=test_env, table_name=table)
        engine.make_engine()
        self.session = sessionmaker(bind=engine.engine)
        self.orm_class = orm_class

    def select(self):
        session = self.session()
        orm = self.orm_class
        return session.query(orm)
