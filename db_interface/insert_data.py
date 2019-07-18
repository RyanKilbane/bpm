from sqlalchemy.orm import sessionmaker
from db_interface.get_metadata import Metadata

class InsertData:
    def __init__(self, database, table, data, orm_class):
        engine = Metadata(test_env=True, table_name=table)
        engine.make_engine()
        self.session = sessionmaker(bind=engine.engine)
        self.data = data
        self.orm_class = orm_class

    def insert(self):
        session = self.session()
        try:
            orm = self.orm_class()
            print(self.data)
            for i in self.data.keys():
                orm.__dict__[i] = self.data[i]
            print(orm.__dict__)
            session.add(orm)
            session.commit()
            return "Data inserted"
        except Exception as error:
            return error
