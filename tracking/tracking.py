from flask import Flask, Blueprint, request
from db_interface.get_metadata import Metadata
from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from exceptions.insert_error import InsertError
from data_operations import DataOperations
from parse_config import config

tracking_point = Blueprint("tracking", __name__)

@tracking_point.route(config["tracking"]["api"], methods=["POST"])
def tracking():
    tracking_table_metadata = Metadata(test_env=config["test"], table_name=config["tracking"]["table_name"], db_name=config["tracking"]["database_name"])
    tracking_table_metadata.make_engine()
    tracking_table_data = tracking_table_metadata.get_table_data()
    data = request.get_json()

    if check_for_no_failures(data):
        return ("Nothing needs tracking\n", 200)

    operations = DataOperations(tracking_table_data, data, config["tracking"]["table_name"], config["tracking"]["stage"], config["tracking"]["database_name"])
    try:
        operations.check(config["tracking"]["ignore"][0])
    except DataError as data_error:
        return ("OH NO! An error\n\n{}\n".format(data_error), 500)
    
    error_table_metadata = Metadata(test_env=config["test"], table_name=config["error"]["table_name"], db_name=config["error"]["database_name"])
    error_table_metadata.make_engine()
    error_table_data = error_table_metadata.get_table_data()
    print(error_table_data)

    errors = DataOperations(error_table_data, {"bpm_id": data["bpm_id"]}, config["error"]["table_name"], config["tracking"]["stage"], config["error"]["database_name"])

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error) + "\n"

    try:
        errors.persist()
    except InsertError as insert_error:
        return str(insert_error) + "\n"
    
    operations.post_to_next_stage("http://127.0.0.1:5000/allocate")

    return ('OK', 200)


@tracking_point.route(config["tracking"]["api"], methods=["PUT"])
def tracking_update():
    table_metadata = Metadata(test_env=config["test"], table_name=config["tracking"]["table_name"], db_name=config["tracking"]["database_name"])
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()
    data = request.get_json()

    if check_for_no_failures(data):
        return ("Nothing needs tracking\n", 200)

    operations = DataOperations(table_data, data, config["tracking"]["table_name"], config["tracking"]["stage"], config["tracking"]["database_name"])
    try:
        operations.check(config["tracking"]["ignore"][0])
    except DataError as data_error:
        return ("OH NO! An error\n\n{}\n".format(data_error), 500)

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error) + "\n"
    
    operations.post_to_next_stage("http://127.0.0.1:5000/allocate")

    return ('OK', 200)

def check_for_no_failures(data):
    if len(data[config["tracking"]["target"]]) == 0:
        return True
    return False
