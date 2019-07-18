from sqlalchemy.orm import sessionmaker
from db_interface.get_metadata import Metadata

class InsertData:
    def __init__(self, database, table, data):
        engine = Metadata(test_env=True, table_name=table)
        engine.make_engine()
        self.session = sessionmaker(bind=engine.engine)
        self.data = data

    def insert(self):
        session = self.session()
        try:
            session.add(self.data)
            session.commit()
            return "Data inserted"
        except Exception as error:
            return error
