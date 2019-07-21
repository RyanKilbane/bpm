from flask import Blueprint, request, render_template
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from db_interface.get_metadata import Metadata
from db_interface.insert_data import InsertData
from db_interface.construct_class import ClassBuild
from exceptions.data_error import DataError
from exceptions.insert_error import InsertError
from data_operations import DataOperations
from parse_config import config

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

@user_point.route(config["users"]["api"], methods=["POST"])
def update_users():
    print("UPDATE")
    form = request.form
    print({key: form[key] for key in form.keys()})


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
