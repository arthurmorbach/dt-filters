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
    Cr : Mapped[float]
    Ch : Mapped[float]
    beta : Mapped[float]
    fs : Mapped[float]
    fc : Mapped[float]
    Zo : Mapped[float]
    time : Mapped[str] = mapped_column(nullable = False)
    tf_points: Mapped[List["TF_Points"]] = relationship(back_populates = 'tf')

class TF_Points(Base):
    __tablename__ = 'tf_point'
    id : Mapped[int] = mapped_column(primary_key = True)
    tf_id : Mapped[int] = mapped_column(ForeignKey('tf.id'), nullable = False) 
    real_part : Mapped[str]
    imaginary_part : Mapped[float]
    tf : Mapped["TF"] = relationship(back_populates = 'tf_point')

Base.metadata.create_all(bind = engine)




