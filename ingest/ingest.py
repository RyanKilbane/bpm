from flask import Blueprint, request
import json
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from db_interface.get_metadata import Metadata
from db_interface.insert_data import InsertData
from db_interface.construct_class import ClassBuild
from exceptions.data_error import DataError
from exceptions.insert_error import InsertError
from data_operations import DataOperations
import time

ingest_point = Blueprint('ingest_point', __name__)

@ingest_point.route('/ingest', methods=["POST"])
def landing():
    table_metadata = Metadata(test_env=True, table_name="ingest", db_name="bpm_test")
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()
    data = request.get_json()

    operations = DataOperations(table_data, data, "ingest", "Ingest", "bpm_test")

    operations.assign_uuid(data)

    try:
        operations.check()
    except DataError as data_error:
        return "OH NO! An error\n\n{}\n".format(data_error)

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error) + "\n"

    return "Data persisted\n"
