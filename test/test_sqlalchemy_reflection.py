import pytest
from test.db_setup import Setup
from db_interface.get_metadata import Metadata

db = Setup("ingest", "bpm_test")
db.create_db()
db.create_ingest_table()

def test_reflection():
    database = Metadata(test_env=True, table_name="ingest", db_name="bpm_test",)
    database.make_engine()
    print(database.get_table_data())
