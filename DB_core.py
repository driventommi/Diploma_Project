
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from config import *

metadata = MetaData()
Base = declarative_base()


class SeenUsers(Base):
    __tablename__ = "viewed"
    bot_user = sq.Column(sq.Integer, primary_key=True)
    shown_user = sq.Column(sq.Integer, primary_key=True)


engine = create_engine(DSN)
Base.metadata.create_all(engine)


def add_in_db(a, i):
    with Session(engine) as session:
        added_in_db = SeenUsers(bot_user=a, shown_user=i)
        session.add(added_in_db)
        session.commit()


def compare(a, i):
    with Session(engine) as session:
        search = session.query(SeenUsers).filter(SeenUsers.bot_user == a).all()
        list_1 = []
        for item in search:
            result = item.shown_user
            list_1.append(result)
        session.commit()
        if i in list_1:
            return True
        else:
            return False
