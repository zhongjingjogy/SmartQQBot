from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from model import Base, PrivateMessage, GroupMessage
import sys
sys.path.append("../")
from smartqq.bot.messages import PrivateMsg, GroupMsg

class DBHandler(object):
    """
    This handler is used to record the messages into a certin database storage.
    """
    def __init__(self, dbhandle='sqlite:///message-record.db'):
        self.dbhandle = dbhandle

        self.create_engine()
        self.create_session()

    def create_engine(self):
        self.engine = create_engine(self.dbhandle)

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_message(self, msg):
        if isinstance(msg, PrivateMsg):
            self.insert_privatemessage(msg)
        elif isinstance(msg, GroupMsg):
            self.insert_groupmessage(msg)
        else:
            print type(msg)
            print("got unknown message type %s" % msg)

    def insert_privatemessage(self, msg):
        pmsg = PrivateMessage(
            poll_type = msg.poll_type,
            msg_id = msg.msg_id,
            msg_type = msg.msg_type,
            from_uin = msg.from_uin,
            to_uin = msg.to_uin,
            content = msg.content,
            recievedtime = msg.time
        )
        try:
            self.session.add(pmsg)
            self.session.commit()
        except:
            print("fail to record private msg")
            self.session.rollback()

    def insert_groupmessage(self, msg):
        gmsg = GroupMessage(
            poll_type = msg.poll_type,
            msg_id = msg.msg_id,
            msg_type = msg.msg_type,
            from_uin = msg.from_uin,
            to_uin = msg.to_uin,
            send_uin = msg.send_uin,
            content = msg.content,
            recievedtime = msg.time
        )
        try:
            self.session.add(gmsg)
            self.session.commit()
        except:
            print("fail to record group msg")
            self.session.rollback()

    def queryall_privatemessage(self):
        return [e for e in self.session.query(PrivateMessage).all()]

    def queryall_groupmessage(self):
        return [e for e in self.session.query(GroupMessage).all()]

if __name__ == "__main__":
    db = MessageDB()
