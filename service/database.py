import pandas as pd

from sqlalchemy import create_engine, Column, Integer, DateTime, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service import settings

engine = create_engine(
    f'postgresql://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}'
)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now)
    user_login = Column(String)
    request = Column(JSON)
    answer = Column(JSON)
    tokens_used = Column(Integer)

    def __init__(self, user_login, request, answer, tokens_used):
        self.user_login = user_login
        self.request = request
        self.answer = answer
        self.tokens_used = tokens_used


def add_history(user_login, request, answer, tokens_used):
    new_row = History(user_login=user_login, request=request, answer=answer, tokens_used=tokens_used)
    session.add(new_row)
    session.commit()


def get_data():
    result = session.query(History).all()

    data = [r.__dict__ for r in result]

    for d in data:
        d.pop('_sa_instance_state', None)

    df = pd.DataFrame(data)
    df = df[History.__table__.columns.keys()]
    df.to_csv("logs.csv", index=False)

    return "logs.csv"


Base.metadata.create_all(engine)
