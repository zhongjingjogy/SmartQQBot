from sqlalchemy import *
from model import Base

def create_db(dbhandle='sqlite:///message-record.db'):
    engine = create_engine(dbhandle)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
