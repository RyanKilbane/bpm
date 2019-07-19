from flask import Flask, Blueprint, request, render_template
from flask_cors import cross_origin
from db_interface.get_metadata import Metadata
from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from exceptions.insert_error import InsertError
from data_operations import DataOperations
from parse_config import config
import time

allocation_point = Blueprint("allocate", __name__)

@allocation_point.route(config["allocations"]["api"], methods=["POST"])
def allocate_post():
    print(config["allocations"]["table_name"])
    allocation_table_metadata = Metadata(test_env=config["test"], table_name=config["allocations"]["table_name"], db_name=config["allocations"]["database_name"])
    allocation_table_metadata.make_engine()
    allocation_table_metadata = allocation_table_metadata.get_table_data()
    data = request.get_json()

    allocate = {"allocated_to": "Alice", "bpm_id": data["bpm_id"], "allocation_date": time.time()}

    operations = DataOperations(allocation_table_metadata, allocate, config["allocations"]["table_name"], config["allocations"]["stage"], config["allocations"]["database_name"])

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error)+"\n"

    return "recived json: {}".format(data)


@allocation_point.route(config["allocations"]["api"], methods=["GET"])
@cross_origin(origin="localhost", headers=["content-Type", "Authorization"])
def allocate_get():
    return "A GET request was recived\n"
