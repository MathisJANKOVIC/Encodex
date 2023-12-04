from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

import database_setup

Base = declarative_base()

class EncodingType(Base):
    __tablename__ = 'encoding_type'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)

    encoding_characters = relationship('EncodingCharacters', backref='encoding_type')

class EncodingCharacters(Base):
    __tablename__ = 'encoding_characters'

    id = Column(Integer, autoincrement=True, primary_key=True)

    character = Column(String(1), nullable=False)
    encoded_character = Column(String(1), nullable=False)

    id_type = Column(Integer, ForeignKey('encoding_type.id'), nullable=False)

Base.metadata.create_all(database_setup.engine)