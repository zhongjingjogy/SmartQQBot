from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from model import Base, PrivateMessage, GroupMessage, Friend
import sys
import datetime
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

    def insert_friend(self, friend_dict):
        birthday = friend_dict[u"birthday"]
        print(type(birthday))
        print("birthday: %s" % birthday)
        friend_dict[u"birthday"] = datetime.datetime(birthday[u"year"], birthday[u"month"], birthday[u"day"])
        friend_dict[u"nickname"] = friend_dict[u"nick"]

        friend = Friend(
            account = friend_dict.get(u"account", ""),
            nickname = friend_dict.get(u"nickname", ""),
            birthday = friend_dict.get(u"birthday", ""),
            gender = friend_dict.get(u"gender", ""),
            province = friend_dict.get(u"province", ""),
            city = friend_dict.get(u"city", ""),
            uin = friend_dict.get(u"uin", ""),
        )

        n = self.session.query(Friend).filter(
            Friend.account == friend_dict[u"account"]
        ).count()
        if n < 1:
            try:
                self.session.add(friend)
                self.session.commit()
            except Exception, e:
                print(e)
                print("fail to add a friend")
                self.session.rollback()
        else:
            pass

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
            recievedtime = msg.time,
            groupname = msg.name
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
