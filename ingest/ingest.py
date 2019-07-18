from flask import Blueprint, request
import json
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from db_interface.get_metadata import Metadata
from db_interface.insert_data import InsertData
from db_interface.construct_class import ClassBuild
from exceptions.data_error import DataError

ingest_point = Blueprint('ingest_point', __name__)

@ingest_point.route('/', methods=["POST"])
def landing():
    table_metadata = Metadata(test_env=True, table_name="ingest", db_name="bpm_test")
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()
    data = request.get_json()
    try:
        check(table_data, data, "bpm_id")
    except DataError as data_error:
        return "OH NO! An error\n\n{}\n".format(data_error)
    
    data_with_id = assign_uuid(data)
    # return str(persist(data_with_id).__dict__)
    return str(persist(data_with_id))

def check(table_metadata, ingest_data, *ignore):
    column_names = [column["name"] for column in table_metadata]
    for attribute in ingest_data["id_info"].keys():
        if attribute not in column_names:
            raise DataError("Ingest data contains too many attributes!\nExpecting: {}\nBut got: {}".format(column_names, ingest_data["id_info"].keys()))
    
    for col in column_names:
        if col not in ingest_data["id_info"].keys() and col not in ignore:
            raise DataError("Ingest data contains too few attributes!\nExpecting: {}\nBut got: {}".format(column_names, ingest_data["id_info"].keys()))

def assign_uuid(ingest_data):
    ingest_data["id_info"]["bpm_id"] = str(uuid4())
    return ingest_data

def persist(data):
    Base = declarative_base()
    ingest_orm = ClassBuild("ingest", data, Base).build_class()
    return InsertData("bpm_test", "ingest", data).insert()
