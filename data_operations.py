from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from exceptions.insert_error import InsertError
from uuid import uuid4

class DataOperations:
    def __init__(self, table_metadata, data, table_name, stage):
        self.table_metadata = table_metadata
        self.data = data
        self.table_name = table_name
        self.stage = stage

    def check(self, *ignore):
        column_names = [column["name"] for column in table_metadata]
        for attribute in self.data.keys():
            if attribute not in column_names:
                raise DataError("{} data contains too many attributes!\nExpecting: {}\nBut got: {}".format(column_names, self.data.keys()))
        
        for col in column_names:
            if col not in self.data.keys() and col not in ignore:
                raise DataError("{} data contains too few attributes!\nExpecting: {}\nBut got: {}".format(column_names, self.data.keys()))

    def assign_uuid(self, data):
        self.data["bpm_id"] = str(uuid4())
        return self.data

    def persist(self):
        Base = declarative_base()
        orm = ClassBuild("ingest", self.data, self.table_metadata, Base).build_class()
        return InsertData("bpm_test", "ingest", self.data, orm).insert()

    def post_to_next_stage(data_to_post):
        pass
