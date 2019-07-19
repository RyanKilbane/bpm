from flask import Flask, Blueprint
from flask_cors import CORS, cross_origin
from ingest.ingest import ingest_point
from tracking.tracking import tracking_point
from allocations.allocate import allocation_point

app = Flask(__name__)
app.register_blueprint(ingest_point)
app.register_blueprint(tracking_point)
app.register_blueprint(allocation_point)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/allocate": {"origins": "http://localhost:3000"}})

app.run(threaded=True)