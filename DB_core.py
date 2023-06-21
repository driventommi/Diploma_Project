# import psycopg2
import pprint
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from config import *

metadata = MetaData()
Base = declarative_base()


class Seen_users(Base):
    __tablename__ = "viewed"
    bot_user = sq.Column(sq.Integer, primary_key=True)
    shown_user = sq.Column(sq.Integer, primary_key=True)


engine = create_engine(DSN)
Base.metadata.create_all(engine)


# Session = sessionmaker(bind=engine)
# session = Session()
def add_in_db(a, i):
    with Session(engine) as session:
        added_in_db = Seen_users(bot_user=a, shown_user=i)
        session.add(added_in_db)
        session.commit()


# def search_db(a):
#     with Session(engine) as session:
#         search = session.query(Seen_users).filter(Seen_users.bot_user == a).all()
#         for item in search:
#             result = item.shown_user
#             return result
#         session.commit()


def compare(a,i):
    with Session(engine) as session:
        search = session.query(Seen_users).filter(Seen_users.bot_user == a).all()
        list_1 = []
        for item in search:
            result = item.shown_user
            list_2 = list_1.append(result)
        session.commit()
        if i in list_1:
            return True
        else:
            return False

    # if i == search_db(a):
    #     return True
    # else:
    #     continue


# session.close()
# def create_db(conn):
#     with conn.cursor() as cur:
#         cur.execute("""
#                 CREATE TABLE IF NOT EXISTS Bot_users(
#                 id SERIAL PRIMARY KEY UNIQUE,
#                 user_id VARCHAR(20) UNIQUE NOT NULL
#                 );
#                 """)
#         cur.execute("""
#         CREATE TABLE IF NOT EXISTS Seen_users(
#         id SERIAL PRIMARY KEY UNIQUE,
#         vkuser_id VARCHAR(20) UNIQUE NOT NULL
#         );
#         """)
#     conn.commit()
#
#
# def add_user():
#
#
# with psycopg2.connect(database=db_name, user=user_db, password=password) as conn:
#     create_db(conn)