from flask import Flask, Blueprint, request
from db_interface.get_metadata import Metadata
from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from exceptions.insert_error import InsertError

tracking_point = Blueprint("tracking", __name__)

@tracking_point.route("/tracking", methods=["POST"])
def tracking():
    table_metadata = Metadata(test_env=True, table_name="tracking", db_name="bpm_test")
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()
    data = request.get_json()

    try:
        check(table_data, data)
    except DataError as data_error:
        return "OH NO! An error\n\n{}\n".format(data_error)

    try:
        persist(data, table_data)
    except InsertError as insert_error:
        return str(insert_error) + "\n"

    return "Data persisted\n"


def check(table_metadata, ingest_data, *ignore):
    column_names = [column["name"] for column in table_metadata]
    for attribute in ingest_data.keys():
        if attribute not in column_names:
            raise DataError("Tracking data contains too many attributes!\nExpecting: {}\nBut got: {}".format(column_names, ingest_data.keys()))
    
    for col in column_names:
        if col not in ingest_data.keys() and col not in ignore:
            raise DataError("Tracking data contains too few attributes!\nExpecting: {}\nBut got: {}".format(column_names, ingest_data.keys()))

def persist(data, column_data):
    Base = declarative_base()
    ingest_orm = ClassBuild("tracking", data, column_data, Base).build_class()
    return InsertData("bpm_test", "tracking", data, ingest_orm).insert()

def post_to_next_stage(data_to_post):
    pass
