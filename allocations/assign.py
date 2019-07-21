from parse_config import config
import time

class AllocateAssign:
    def __init__(self, data, db_engine):
        self.data = data
        self.engine = db_engine
    
    def get_oldest(self):
        users = self.engine.execute("SELECT user from {} WHERE should_allocate = 'Y' ORDER BY last_assigned ASC".format(config["users"]["table_name"]))
        return list(users)[0]

    def assign(self, user_info):
        return {"allocated_to": user_info[0], "bpm_id": self.data["bpm_id"], "allocation_date": time.time()}

    def update_users(self, user_info):
        self.engine.execute("UPDATE {} SET last_assigned = {} WHERE user = '{}'".format(config["users"]["table_name"], time.time(), user_info[0]))
