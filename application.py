from flask import Flask, Blueprint
from ingest.ingest import ingest_point

app = Flask(__name__)
app.register_blueprint(ingest_point)

app.run()