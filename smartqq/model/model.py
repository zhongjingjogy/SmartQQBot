from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    poll_type = Column(String(20))
    msg_id = Column(Integer)
    msg_type = Column(Integer)
    from_uin = Column(Integer)
    to_uin = Column(Integer)
    content = Column(String(255))
    recievedtime = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        items = ["id", "poll_type", "from_uin", "msg_id", "msg_type", "to_uin", "content", "time"]
        values = [self.id, self.poll_type, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content,  self.recievedtime]
        return "Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())

class PrivateMessage(Message):
    __tablename__ = "privatemessage"
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    nickname = Column(String(100))
    def __str__(self):
        items = ["id", "poll_type", "from_uin", "msg_id", "msg_type", "to_uin", "content", "time"]
        values = [self.id, self.poll_type, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content,  self.recievedtime]
        return "Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())

class GroupMessage(Message):
    __tablename__ = "groupmessage"
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    group_code = Column(Integer)
    send_uin = Column(Integer)
    groupname = Column(String(50))
    def __str__(self):
        items = ["poll_type", "group_code", "send_uin", "from_uin", "msg_id", "msg_type", "to_uin", "content", "time"]
        values = [self.poll_type, self.group_code, self.send_uin, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content, self.recievedtime]
        return "Group Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())

class SaturoRecord(Base):
    __tablename__ = "saturorecord"
    key = Column(String(100), primary_key=True)
    value = Column(String(200))

    def __str__(self):
        return "\{{key}: {value}\}".format(key=self.key, value=self.value)

    def __unicode__(self):
        return unicode(self.__str__())

class Friend(Base):
    __tablename__ = "friend"
    id = Column(Integer, primary_key=True)
    account = Column(Integer)
    nickname = Column(String(100))
    birthday = Column(DateTime, default=datetime.utcnow)
    gender = Column(String(20))
    province = Column(String(20))
    city = Column(String(20))
    uin = Column(Integer)
    def __str__(self):
        items = ["account", "nickname", "birthday", "gender", "province", "city", "uin"]
        items = [self.account, self.nickname, self.birthday, self.gender, self.province, self.city, self.uin]
        return "Friend : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())
