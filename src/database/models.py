from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
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
    is_case_sensitive = Column(Boolean, nullable=False)

    encoded_chars_sep = Column(String(255), nullable=True)
    encoded_words_sep = Column(String(255), nullable=True)
    encoded_chars_len = Column(Integer, nullable=True)

    encoding_chars = relationship('EncodingChar', backref='encoding_types')

    def __init__(self, name: str, encoding_chars: dict, is_case_sensitive: bool, encoded_chars_sep: str, encoded_words_sep: str, encoded_chars_len: int | None):
        self.name = name
        for char, encoding_char in encoding_chars.items():
            self.encoding_chars.append(EncodingChar(char, encoding_char))

        self.is_case_sensitive = is_case_sensitive

        self.encoded_chars_sep = encoded_chars_sep
        self.encoded_words_sep = encoded_words_sep
        self.encoded_chars_len = encoded_chars_len

    def dict(self) -> dict:
        """Returns a dictionary representation of EncodingType object"""
        return {
            "id": self.id,
            "name": self.name,
            "is_case_sensitive": self.is_case_sensitive,
            "encoded_chars_sep": self.encoded_chars_sep,
            "encoded_words_sep": self.encoded_words_sep,
            "encoded_chars_len": self.encoded_chars_len,
            "encoding_chars": {encoding_char.char: encoding_char.encoded_char for encoding_char in self.encoding_chars}
        }

    def encoded_char(self, char: str) -> str:
        """Returns the encoded version of `char` if exists in the encoding character set otherwise returns `char`"""
        return next((encoding_char.encoded_char for encoding_char in self.encoding_chars if encoding_char.char == char), char)

    def decoded_char(self, encoded_char: str) -> str:
        """Returns the decoded version of `decoded_char` if exists in the encoding character set otherwise returns `decoded_char`"""
        return next((encoding_char.char for encoding_char in self.encoding_chars if encoding_char.encoded_char == encoded_char), encoded_char)

if(__name__ == '__main__'):
    Base.metadata.drop_all(connection.engine)
    Base.metadata.create_all(connection.engine)
