from flask import Blueprint

ingest_point = Blueprint('ingest_point', __name__)

@ingest_point.route('/', methods=["POST"])
def landing():
    pass