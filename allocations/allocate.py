from flask import Flask, Blueprint, request, render_template, render_template_string
from flask_cors import cross_origin
from db_interface.get_metadata import Metadata
from exceptions.data_error import DataError
from sqlalchemy.ext.declarative import declarative_base
from db_interface.construct_class import ClassBuild
from db_interface.insert_data import InsertData
from exceptions.insert_error import InsertError
from data_operations import DataOperations
from parse_config import config
from allocations.assign import AllocateAssign
import time

allocation_point = Blueprint("allocate", __name__)

@allocation_point.route(config["allocations"]["api"], methods=["POST"])
def allocate_post():
    allocation_table_metadata = Metadata(test_env=config["test"], table_name=config["allocations"]["table_name"], db_name=config["allocations"]["database_name"])
    allocation_table_metadata.make_engine()
    connect = allocation_table_metadata.engine.connect()
    allocation_table_metadata = allocation_table_metadata.get_table_data()
    data = request.get_json()

    allocate_assign = AllocateAssign(data, connect)
    oldest = allocate_assign.get_oldest()
    allocate = allocate_assign.assign(oldest)
    allocate_assign.update_users(oldest)

    operations = DataOperations(allocation_table_metadata, allocate, config["allocations"]["table_name"], config["allocations"]["stage"], config["allocations"]["database_name"])

    try:
        operations.persist()
    except InsertError as insert_error:
        return str(insert_error)+"\n"

    return "recived json: {}".format(data)


@allocation_point.route(config["allocations"]["api"], methods=["GET"])
@cross_origin(origin="localhost", headers=["content-Type", "Authorization"])
def allocate_get():
    allocation_table_metadata = Metadata(test_env=config["test"], table_name=config["allocations"]["table_name"], db_name=config["allocations"]["database_name"])
    allocation_table_metadata.make_engine()

    connect = allocation_table_metadata.engine.connect()

    results = connect.execute("select * from {}".format(config["allocations"]["table_name"]))
    users = connect.execute("SELECT * FROM {}".format(config["users"]["table_name"]))
    headers=["ID", "Assigned to", "Assigned on"]

    records = build_json(headers, results)

    return render_template("./view_allocations.html", header=headers, records=records, users=users, cr_url=config["cr_redirect"])

@allocation_point.route(config["allocations"]["api"], methods=["PUT"])
def allocate_update():
    pass

def build_json(headers, records):
    return [dict(zip(headers, i)) for i in list(records)]
