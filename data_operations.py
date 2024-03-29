from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from db_interface.get_data import QueryData
from exceptions.insert_error import InsertError
from uuid import uuid4
import requests
from parse_config import config
import json

class DataOperations:
    def __init__(self, table_metadata, data, table_name, stage, db_name):
        self.table_metadata = table_metadata
        self.data = data
        self.table_name = table_name
        self.stage = stage
        self.db = db_name
        
    def check(self, *ignore):
        column_names = [column["name"] for column in self.table_metadata]
        for attribute in self.data.keys():
            if attribute not in column_names and attribute not in ignore:
                raise DataError("{} data contains too many attributes!\nExpecting: {}\nBut got: {}".format(self.stage, column_names, self.data.keys()))
        
        for col in column_names:
            if col not in self.data.keys() and col not in ignore:
                raise DataError("{} data contains too few attributes!\nExpecting: {}\nBut got: {}".format(self.stage, column_names, self.data.keys()))

    def assign_uuid(self):
        self.data["bpm_id"] = str(uuid4())

    def persist(self):
        Base = declarative_base()
        orm = ClassBuild(self.table_name, self.data, self.table_metadata, Base).build_class()
        return InsertData(self.db, self.table_name, self.data, orm, config["test"]).insert()

    def select(self):
        Base = declarative_base()
        orm = ClassBuild(self.table_name, {}, self.table_metadata, Base).build_class()
        return QueryData(self.db, self.table_name, orm, config["test"]).select()

    def update(self, filter_attribute, filter_value, value_to_update, updated_value, update_data):
        Base = declarative_base()
        orm = ClassBuild(self.table_name, self.data, self.table_metadata, Base).build_class()
        return QueryData(self.db, self.table_name, orm, config["test"]).update(filter_attribute, filter_value, value_to_update, updated_value, update_data)
        

    def post_to_next_stage(self, api):
        print("data to post: {}".format(self.data))
        requests.post(url=api, data=json.dumps(self.data), headers={"content-type": "application/json"})
