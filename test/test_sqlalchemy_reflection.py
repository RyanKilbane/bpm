import pytest
from db_setup import Setup
from db_interface.get_metadata import Metadata

db = Setup(ingest_table="ingest", tracking_table="tracking", db_name="bpm_test")
db.create_db()
db.create_ingest_table()
db.create_tracking_table()

def test_reflection():
    database = Metadata(test_env=True, table_name="ingest", db_name="bpm_test",)
    database.make_engine()
    cols = database.get_table_data()
    columns = []
    for i in cols:
        columns.append(i["name"])
    assert sorted(columns) == sorted(["reference", "period", "survey", "bpm_id"])
