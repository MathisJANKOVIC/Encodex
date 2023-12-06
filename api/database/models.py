from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from database import connection

Base = declarative_base()

class EncodingCharacter(Base):
    __tablename__ = 'encoding_character'

    id = Column(Integer, primary_key=True, autoincrement=True)

    char = Column(String(1), nullable=False)
    encoded_char = Column(String(255), nullable=False)

    id_encoding_type = Column(Integer, ForeignKey('encoding_type.id'), nullable=False)

    def __init__(self, char: str, encoded_char: str):
        self.char = char
        self.encoded_char = encoded_char

class EncodingType(Base):
    __tablename__ = 'encoding_type'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)

    encoding_chars = relationship('EncodingCharacter', backref='encoding_type')

    def __init__(self, name: str, encoding_characters: dict):
        self.name = name
        for char, encoding_char in encoding_characters.items():
            self.encoding_chars.append(EncodingCharacter(char, encoding_char))

if(__name__ == '__main__'):
    Base.metadata.create_all(connection.engine)
