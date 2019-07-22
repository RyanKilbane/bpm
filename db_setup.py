import sqlite3 as sl
import time
from db_interface.get_metadata import Metadata

class Setup:
    def __init__(self, ingest_table, tracking_table, error_table, allocation_table, user_table, db_name):
        self.db = None
        self.ingest_table = ingest_table
        self.tracking_table = tracking_table
        self.error_table = error_table
        self.allocation_table = allocation_table
        self.user_table = user_table
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
                        PRIMARY KEY (bpm_id));".format(self.tracking_table)
        cursor = self.db.cursor()
        cursor.execute(tracking_table)

    def create_error_table(self):
        error_table = "CREATE TABLE {} (\
                        bpm_id varchar(50) UNIQUE NOT NULL, \
                        PRIMARY KEY (bpm_id));".format(self.error_table)
        cursor = self.db.cursor()
        cursor.execute(error_table)

    def create_allocation_table(self):
        allocation_table = "CREATE TABLE {} (\
                        bpm_id varchar(50) UNIQUE NOT NULL, \
                        allocated_to varchar(50) NOT NULL, \
                        allocation_date INTEGER NOT NULL, \
                        PRIMARY KEY (bpm_id), \
                        FOREIGN KEY (bpm_id) REFERENCES {}(bmp_id)\
                        FOREIGN KEY (allocated_to) REFERENCES {}(user));".format(self.allocation_table, self.tracking_table, self.user_table)
        cursor = self.db.cursor()
        cursor.execute(allocation_table)

    def create_user_table(self):
        user_table = "CREATE TABLE {} (\
                      user VARCHAR(6) UNIQUE NOT NULL,\
                      last_assigned INTEGER,\
                      should_allocate CHAR(1),\
                      PRIMARY KEY (user));".format(self.user_table)
        cursor = self.db.cursor()
        cursor.execute(user_table)

    def populate_users(self):
        insert_users = "INSERT INTO {} VALUES ('alice', {}, 'Y')".format(self.user_table, time.time())
        cursor = self.db.cursor()
        cursor.execute(insert_users)
        self.db.commit()
        insert_users = "INSERT INTO {} VALUES ('bob', {}, 'Y')".format(self.user_table, time.time())
        cursor = self.db.cursor()
        cursor.execute(insert_users)
        self.db.commit()
        insert_users = "INSERT INTO {} VALUES ('eve', {}, 'N')".format(self.user_table, time.time())
        cursor = self.db.cursor()
        cursor.execute(insert_users)
        self.db.commit()

db = Setup(ingest_table="ingest", tracking_table="tracking", error_table="errors", allocation_table="allocations", user_table="users", db_name="bpm_test")
db.create_db()
db.create_ingest_table()
db.create_tracking_table()
db.create_error_table()
db.create_allocation_table()
db.create_user_table()
db.populate_users()
