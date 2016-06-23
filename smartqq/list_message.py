#coding=utf-8
import sys
from model.dbhandler import DBHandler

def list_messages():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    handler = DBHandler()

    for each in handler.queryall_privatemessage():
        print(each)

    for each in handler.queryall_groupmessage():
        print(each)
