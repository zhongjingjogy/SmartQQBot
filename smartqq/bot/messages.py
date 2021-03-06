# coding: utf-8
import datetime

PRIVATE_MSG = "message"
GROUP_MSG = "group_message"
SESS_MSG = "sess_message"
INPUT_NOTIFY_MSG = "input_notify"
KICK_MSG = "kick_message"
DISCU_MSG = "discu_message"
# Msg type in message content
OFF_PIC_PART = "offpic"
C_FACE_PART = "cface"

OFF_PIC_PLACEHOLDER = "[图片]"
C_FACE_PLACEHOLDER = "[表情]"


class QMessage(object):

    def __init__(self, msg_dict):
        self.meta = msg_dict

        self.poll_type = msg_dict['poll_type']
        value = msg_dict['value']

        self.from_uin = value['from_uin']
        self.msg_id = value['msg_id']
        self.msg_type = value['msg_type']
        self.to_uin = value['to_uin']
        self._content = value['content']
        self._time = value['time']
        self.font = None

        for i in value['content']:
            if isinstance(i, list) and i[0] == "font":
                self.font = i[1]
    @property
    def time(self):
        return datetime.datetime.fromtimestamp(self._time)
    @property
    def content(self):
        text = ""
        for msg_part in self._content:
            if isinstance(msg_part, (str, unicode)):
                text += msg_part
            elif len(msg_part) > 1:
                if str(msg_part[0]) == OFF_PIC_PART:
                    text += OFF_PIC_PLACEHOLDER
                elif str(msg_part[0]) == C_FACE_PART:
                    text += C_FACE_PLACEHOLDER

        return text

    @property
    def type(self):
        return self.poll_type

    def __str__(self):
        items = ["poll_type", "from_uin", "msg_id", "msg_type", "to_uin", "content", "_content", "time", "font"]
        values = [self.poll_type, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content, self._content, self.time, self.font]
        return "Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])

    def __unicode__(self):
        return unicode(self.__str__())


class SessMsg(QMessage):
    """
    临时会话消息
    """

    def __init__(self, msg_dict):
        super(SessMsg, self).__init__(msg_dict)
        self.service_type = msg_dict['value']['service_type']
        self.id = msg_dict['value']['id']
        self.ruin = msg_dict['value']['ruin']
        self.flags = msg_dict['value']['flags']


class PrivateMsg(QMessage):
    def __init__(self, msg_dict):
        super(PrivateMsg, self).__init__(msg_dict)
        self.to_uin = msg_dict['value']['to_uin']
        self.from_uin = msg_dict['value']['from_uin']
    def __str__(self):
        items = ["poll_type", "from_uin", "msg_id", "msg_type", "to_uin", "content", "_content", "time", "font"]
        values = [self.poll_type, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content, self._content, self.time, self.font]
        return "Private Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())

class GroupMsg(QMessage):

    def __init__(self, msg_dict):
        super(GroupMsg, self).__init__(msg_dict)
        self.group_code = msg_dict['value']['group_code']
        self.send_uin = msg_dict['value']['send_uin']
        self.from_uin = msg_dict['value']['from_uin']
        self.name = ""
    def __str__(self):
        items = ["name", "poll_type", "group_code", "send_uin", "from_uin", "msg_id", "msg_type", "to_uin", "content", "_content", "time", "font"]
        values = [self.name, self.poll_type, self.group_code, self.send_uin, self.from_uin, self.msg_id, self.msg_type, self.to_uin, self.content, self._content, self.time, self.font]
        return "Group Message : \n\t" + "\n\t".join(["%s : %s" % (k, v) for k, v in zip(items, values)])
    def __unicode__(self):
        return unicode(self.__str__())

class DiscuMsg(QMessage):

    def __init__(self, msg_dict):
        super(DiscuMsg, self).__init__(msg_dict)

MSG_TYPE_MAP = {
    GROUP_MSG: GroupMsg,
    INPUT_NOTIFY_MSG: QMessage,
    KICK_MSG: QMessage,
    SESS_MSG: SessMsg,
    PRIVATE_MSG: PrivateMsg,
    DISCU_MSG: DiscuMsg
}


def mk_msg(msg_dict):
    return MSG_TYPE_MAP[msg_dict['poll_type']](msg_dict)
