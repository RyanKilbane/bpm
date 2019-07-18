import sqlite3 as sl
from db_interface.get_metadata import Metadata

class Setup:
    def __init__(self, ingest_table, tracking_table, db_name):
        self.db = None
        self.ingest_table = ingest_table
        self.tracking_table = tracking_table
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
                        reference varchar(11),\
                        period varchar(6), \
                        survey varchar(4), \
                        bpm_id varchar(50) unique, \
                        PRIMARY KEY (reference, period, survey));".format(self.ingest_table)
        cursor = self.db.cursor()
        cursor.execute(ingest_table)

    def create_tracking_table(self):
        tracking_table = "CREATE TABLE {} (\
                        reference varchar(11) NOT NULL,\
                        period varchar(6) NOT NULL, \
                        survey varchar(4) NOT NULL, \
                        bpm_id varchar(50) UNIQUE NOT NULL, \
                        stage varchar(50) NOT NULL, \
                        PRIMARY KEY (reference, period, survey));".format(self.tracking_table)
        cursor = self.db.cursor()
        cursor.execute(tracking_table)
