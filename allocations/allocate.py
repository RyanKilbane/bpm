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

allocation_point = Blueprint("allocate", __name__)

@allocation_point.route(config["allocations"]["api"], methods=["POST"])
def allocate_post():
    data = request.get_json()
    return "recived json: {}".format(data)


@allocation_point.route(config["allocations"]["api"], methods=["GET"])
@cross_origin(origin="localhost", headers=["content-Type", "Authorization"])
def allocate_get():
    return "A GET request was recived\n"
