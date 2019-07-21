from flask import Flask, Blueprint
from flask_cors import CORS, cross_origin
from ingest.ingest import ingest_point
from tracking.tracking import tracking_point
from allocations.allocate import allocation_point
from dashboard.dashboard import dashboard_point
from metrics.metrics import metric_point
from users.users import user_point

app = Flask(__name__, template_folder="templates")
app.register_blueprint(ingest_point)
app.register_blueprint(tracking_point)
app.register_blueprint(allocation_point)
app.register_blueprint(dashboard_point)
app.register_blueprint(metric_point)
app.register_blueprint(user_point)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/allocate": {"origins": "http://localhost:3000"}})

app.run(threaded=True)
