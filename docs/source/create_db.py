from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base, sessionmaker, DeclarativeBase
from sqlalchemy import ForeignKey, UniqueConstraint, create_engine, Text, JSON
from datetime import datetime
import os
from typing import List, Optional

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///" + os.path.join(BASE_DIR, 'tf.db')
Base = declarative_base()
engine = create_engine(connection_string, echo = True)

Session = sessionmaker()

class TF(Base):
    __tablename__ = 'tf'
    id : Mapped[int] = mapped_column(primary_key = True)
    tf_name : Mapped[str]
    filter_type : Mapped[str]
    Cr : Mapped[str]
    Ch : Mapped[str]
    beta : Mapped[str]
    fs : Mapped[str]
    fc : Mapped[str]
    Zo : Mapped[str]
    time : Mapped[str] = mapped_column(nullable = False)

Base.metadata.create_all(bind = engine)