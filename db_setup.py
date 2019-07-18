import sqlite3 as sl
from db_interface.get_metadata import Metadata

class Setup:
    def __init__(self, table, db_name):
        self.db = None
        self.table = table
        self.db_name = db_name

    def create_db(self):
        try:
            connect = sl.connect(self.db_name)
            self.db = connect
        except Exception as e:
            print(e)
            connect.close()
    
    def create_ingest_table(self):
        ingest_table = "CREATE TABLE {} (\
                        reference varchar(11) unique,\
                        period varchar(6), \
                        survey varchar(4), \
                        bpm_id varchar(50) unique \
                        );".format(self.table)
        cursor = self.db.cursor()
        cursor.execute(ingest_table)

    def insert_test(self):
        insert_into = """ INSERT INTO {} VALUES (12345678900, 202009, 123, None)""".format(self.table)

# db = Setup("ingest", "bpm_test")
# db.create_db()
# db.create_ingest_table()
# db.insert_test()

# database = Metadata(test_env=True, table_name="ingest", db_name="bpm_test")
# database.make_engine()
# print(database.get_table_data())
