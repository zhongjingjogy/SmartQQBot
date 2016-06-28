from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()

"""
poll_type : message
    from_uin : 2895548428
    msg_id : 48558
    msg_type : 0
    to_uin : 260700286
    content :
    _content : [[u'font', {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5fae\u8f6f\u96c5\u9ed1', u'size': 10}], [u'face', 5]]
    time : 2016-06-23 18:46:38
    font : {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5fae\u8f6f\u96c5\u9ed1', u'size': 10}
"""

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
