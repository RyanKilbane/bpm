from flask import Blueprint, request, render_template
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from db_interface.get_metadata import Metadata
from db_interface.insert_data import InsertData
from db_interface.construct_class import ClassBuild
from exceptions.data_error import DataError
from exceptions.insert_error import InsertError
from exceptions.update_error import UpdateError
from data_operations import DataOperations
from parse_config import config
import time

user_point = Blueprint("user", __name__)

@user_point.route(config["users"]["api"], methods=["GET"])
def get_users():
    table_metadata = Metadata(test_env=config["test"], table_name=config["users"]["table_name"], db_name=config["users"]["database_name"])
    table_metadata.make_engine()
    table_data = table_metadata.get_table_data()

    operations = DataOperations(table_data, {}, config["users"]["table_name"], config["users"]["stage"], config["users"]["database_name"])

    user_objects = operations.select()
    records = build_json(user_objects)
    headers = records[0].keys()

    # return ("Data returned", 200)
    return render_template("./view_users.html", records=records, headers=sorted(headers))

@user_point.route(config["users"]["api"], methods=["PUT"])
def update_users():
    table_metadata = Metadata(test_env=config["test"], table_name=config["users"]["table_name"], db_name=config["users"]["database_name"])
    table_metadata.make_engine()
    # table_data = table_metadata.get_table_data()

    data = request.get_json()
    # data["last_allocated"] = time.time()

    # operations = DataOperations(table_data, data, config["users"]["table_name"], config["users"]["stage"], config["users"]["database_name"])
    # print("Create DataOperations instance")
    try:
        conn = table_metadata.engine.connect()
        conn.execute("UPDATE {} SET should_allocate = '{}' WHERE user = '{}'".format(config["users"]["table_name"], data["should_allocate"], data["user"]))
        return ("updated\n", 200)
    except Exception as error:
        return (str(error) + "\n", 500)


def build_json(objects):
    return_list = []
    for i in objects:
        temp_dict = {}
        for j in i.__dict__.keys():
            if j in ("_sa_instance_state"):
                continue
            temp_dict[j] = i.__dict__[j]
        return_list.append(temp_dict)
    return return_list
