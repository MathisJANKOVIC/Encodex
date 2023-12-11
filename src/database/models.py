from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from database import connection

Base = declarative_base()

class EncodingChar(Base):
    __tablename__ = 'encoding_characters'

    id = Column(Integer, autoincrement=True, primary_key=True)

    char = Column(String(1), nullable=False)
    encoded_char = Column(String(255), nullable=False)

    encoding_type_id = Column(Integer, ForeignKey('encoding_types.id'), nullable=False)

    def __init__(self, char: str, encoded_char: str):
        self.char = char
        self.encoded_char = encoded_char

class EncodingType(Base):
    __tablename__ = 'encoding_types'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    encoded_chars_sep = Column(String(255), nullable=True)
    encoded_words_sep = Column(String(255), nullable=True)
    encoded_chars_len = Column(Integer, nullable=True)
    encoding_chars = relationship('EncodingChar', backref='encoding_types')

    def __init__(self, name: str, encoding_chars: dict, encoded_chars_sep: str, encoded_words_sep: str, encoded_chars_len: int | None):
        self.name = name
        for char, encoding_char in encoding_chars.items():
            self.encoding_chars.append(EncodingChar(char, encoding_char))

        self.encoded_chars_sep = encoded_chars_sep
        self.encoded_words_sep = encoded_words_sep
        self.encoded_chars_len = encoded_chars_len

if(__name__ == '__main__'):
    Base.metadata.drop_all(connection.engine)
    Base.metadata.create_all(connection.engine)
