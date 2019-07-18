from flask import Flask, Blueprint
from ingest.ingest import ingest_point
from tracking.tracking import tracking_point
from allocations.allocate import allocation_point

app = Flask(__name__)
app.register_blueprint(ingest_point)
app.register_blueprint(tracking_point)
app.register_blueprint(allocation_point)

app.run(threaded=True)