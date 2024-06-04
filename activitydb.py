import os
from common.log import logger
from tinydb import TinyDB, Query


class ActivityDB:
    def __init__(self) -> None:
        self.curdir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.curdir, "activity.json")
        self.db = TinyDB(self.db_path)
        self.activity_query = Query()

    def query_activity(self,
                       activity_name: str):
        return self.db.search(self.activity_query.activity_name == activity_name)

    def add_activity(self,
                     activity_name: str,
                     describe: str,
                     number: int):
        if len(self.query_activity(activity_name)) == 0 and activity_name != "":
            self.db.insert({'activity_name': activity_name, 'describe': describe, "number": number, "member": []})
            logger.info(f"[Solitaire] Create activity:{activity_name} success!")
            return True
        else:
            logger.info(f"[Solitaire] Create activity:{activity_name} fail, this activity is already exist!")
            return False

    def del_activity(self,
                     activity_name: str):
        if len(self.query_activity(activity_name)) != 0:
            self.db.remove(self.activity_query.activity_name == activity_name)
            logger.info(f"[Solitaire] Remove activity:{activity_name} success!")
            return True
        else:
            logger.info(f"[Solitaire] Remove activity:{activity_name} fail, this activity is not exist!")
            return False

    def add_member(self,
                   activity_name: str,
                   member_name: str):
        try:
            result = self.db.search(self.activity_query.activity_name == activity_name)[0]

            number = result["number"]
            member = result["member"]

            if len(member) != number:
                member.append(member_name)
                logger.info(f"[Solitaire] add member:{member_name} success!")
                self.db.update({'member': member}, self.activity_query.activity_name == activity_name)
                return True
            else:
                logger.info(f"[Solitaire] no more please for anyone!")

        except Exception as e:
            logger.error(f"[Solitaire] ERROR: {e}")

        return False

    def del_member(self,
                   activity_name: str,
                   member_name: str):

        try:
            result = self.db.search(self.activity_query.activity_name == activity_name)[0]
            number = result["number"]
            member = result["member"]

            if member_name in member:
                member.remove(member_name)
                logger.info(f"[Solitaire] remove member:{member_name} success!")
                self.db.update({'member': member}, self.activity_query.activity_name == activity_name)
                return True
            else:
                logger.info(f"[Solitaire] member:{member_name} not in List!")

        except Exception as e:
            logger.error(f"[Solitaire] ERROR: {e}")

        return False

    def get_all_data(self):
        return self.db.all()
