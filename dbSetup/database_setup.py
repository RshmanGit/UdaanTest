from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from serveCreds import serve

Base = declarative_base()

class screen(Base):
    __tablename__ = 'screen'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False, unique = True)

    rows = relationship('row', back_populates="screen")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @property
    def ref(self):
        return {
            'name': self.name
        }

class row(Base):
    __tablename__ = 'row'

    id = Column(Integer, primary_key = True)
    name = Column(String(5), nullable = False)

    screenid = Column(Integer, ForeignKey('screen.id'))
    screen = relationship("screen", back_populates='rows')

    seats = relationship('seat', back_populates="row")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'row': self.name,
            'screen': self.screen.ref
        }

    @property
    def row(self):
        return {
            'row': self.name,
            'screen': self.screen.ref
        }

class seat(Base):
    __tablename__ = 'seat'

    id = Column(Integer, primary_key = True)
    number = Column(Integer, nullable = False)
    booked = Column(Boolean, default = False)
    aisle = Column(Boolean, default = False)

    rowid = Column(Integer, ForeignKey('row.id'))
    row = relationship("row", back_populates="seats")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'seatNumber': self.number,
            'row': self.row.ref
        }


def run():
    engine = create_engine(serve())
    Base.metadata.create_all(engine)