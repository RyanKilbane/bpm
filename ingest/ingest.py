from flask import Blueprint, request
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from db_interface.get_metadata import Metadata
from db_interface.insert_data import InsertData
from db_interface.construct_class import ClassBuild
from exceptions.data_error import DataError
from exceptions.insert_error import InsertError
from data_operations import DataOperations
from parse_config import config

ingest_point = Blueprint('ingest_point', __name__)

@ingest_point.route(config["ingest"]["api"], methods=["POST"])
def landing():
    table_metadata = Metadata(test_env=config["test"], table_name=config["ingest"]["table_name"], db_name=config["ingest"]["database_name"])
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()
    data = request.get_json()

    operations = DataOperations(table_data, data, config["ingest"]["table_name"], config["ingest"]["stage"], config["ingest"]["database_name"])

    try:
        operations.check(config["ingest"]["ignore"][0])
    except DataError as data_error:
        return "OH NO! An error\n\n{}\n".format(data_error)

    operations.assign_uuid()

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error) + "\n"

    # TODO: Add POST to data prep stage

    return ("Data persisted\n", 200)
