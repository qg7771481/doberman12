from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


standart_db = "sqlite:///app.db"

engine = create_engine(
    "%s" % standart_db, echo=True
)
Session = sessionmaker(bind=engine)
session = Session

class Base(DeclarativeBase):
    ...
