from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from database import connection

Base = declarative_base()

class CodePoint(Base):
    __tablename__ = 'charset'

    id = Column(Integer, autoincrement=True, primary_key=True)

    char = Column(String(1), nullable=False)
    encoded_char = Column(String(255), nullable=False)

    encoding_standard_id = Column(Integer, ForeignKey('encoding_standard.id'), nullable=False)

    def __init__(self, char: str, encoded_char: str):
        self.char = char
        self.encoded_char = encoded_char

class EncodingStandard(Base):
    __tablename__ = 'encoding_standard'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    case_sensitive = Column(Boolean, nullable=False)
    allowed_unrefenced_chars = Column(Boolean, default=False)

    encoded_char_len = Column(Integer)
    encoded_char_sep = Column(String(255), nullable=False)

    charset = relationship('CodePoint', backref='encoding_standard')

    def __init__(self,
            name: str,
            case_sensitive: bool,
            allowed_unrefenced_chars: bool,
            encoded_char_len: int | None,
            encoded_char_sep: str,
            charset: dict[str, str]
        ):
        self.name = name
        self.case_sensitive = case_sensitive
        self.allowed_unrefenced_chars = allowed_unrefenced_chars

        self.encoded_char_len = encoded_char_len
        self.encoded_char_sep = encoded_char_sep

        for char, encoding_char in charset.items():
            self.charset.append(CodePoint(char, encoding_char))

    def dict(self) -> dict:
        """Returns a dictionary representation of the object"""
        return {
            "name": self.name,
            "case_sensitive": self.case_sensitive,
            "allowed_unrefenced_chars": self.allowed_unrefenced_chars,
            "encoded_char_len": self.encoded_char_len,
            "encoded_char_sep": self.encoded_char_sep,
            "charset": {encoding_char.char: encoding_char.encoded_char for encoding_char in self.charset}
        }

    def encode(self, char: str) -> str | None:
        """Returns the encoded version of `char` if exists in the charset otherwise returns None"""
        return self.dict()['charset'].get(char)

    def decode(self, encoded_char: str) -> str | None:
        """Returns the encoded version of `encoded_char` if exists in the charset otherwise returns None"""
        for char, encoded_character in self.dict()['charset'].items():
            if(encoded_character == encoded_char):
                return char
        return None

if(__name__ == '__main__'):
    Base.metadata.drop_all(connection.engine)
    Base.metadata.create_all(connection.engine)
