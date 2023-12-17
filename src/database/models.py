from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from database import connection

Base = declarative_base()

class CodePoint(Base):
    __tablename__ = 'code_points'

    id = Column(Integer, autoincrement=True, primary_key=True)

    char = Column(String(1), nullable=False)
    encoded_char = Column(String(255), nullable=False)

    encoding_standard_id = Column(Integer, ForeignKey('char_encoding_standards.id'), nullable=False)

    def __init__(self, char: str, encoded_char: str):
        self.char = char
        self.encoded_char = encoded_char

class EncodingStandard(Base):
    __tablename__ = 'char_encoding_standards'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    case_sensitive = Column(Boolean, nullable=False)
    allowed_unrefenced_chars = Column(Boolean, default=False)

    encoded_char_len = Column(Integer)
    encoded_char_sep = Column(String(255), nullable=False)
    encoded_word_sep = Column(String(255), nullable=False)

    charset = relationship('CodePoint', backref='char_encoding_standards')

    @property
    def dict(self) -> dict:
        """Returns a dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "case_sensitive": self.case_sensitive,
            "allowed_unrefenced_chars": self.allowed_unrefenced_chars,
            "encoded_char_len": self.encoded_char_len,
            "encoded_char_sep": self.encoded_char_sep,
            "encoded_word_sep": self.encoded_word_sep,
            "charset": {encoding_char.char: encoding_char.encoded_char for encoding_char in self.charset}
        }

    def __init__(self,
            name: str,
            case_sensitive: bool,
            allowed_unrefenced_chars: bool,
            encoded_char_len: int | None,
            encoded_char_sep: str,
            encoded_word_sep: str,
            charset: dict[str, str]
        ):
        self.name = name
        self.case_sensitive = case_sensitive
        self.allowed_unrefenced_chars = allowed_unrefenced_chars

        self.encoded_char_len = encoded_char_len
        self.encoded_char_sep = encoded_char_sep
        self.encoded_word_sep = encoded_word_sep

        for char, encoding_char in charset.items():
            self.charset.append(CodePoint(char, encoding_char))

    def encode_char(self, char: str) -> str | None:
        """Returns the encoded version of `char` if exists in the charset otherwise returns None"""
        for code_point in self.charset:
            if(code_point.char == char):
                return code_point.encoded_char
        return None

    def decode_char(self, encoded_char: str) -> str | None:
        """Returns the encoded version of `encoded_char` if exists in the charset otherwise returns None"""
        for code_point in self.charset:
            if(code_point.encoded_char == encoded_char):
                return code_point.encoded_char
        return None

if(__name__ == '__main__'):
    Base.metadata.drop_all(connection.engine)
    Base.metadata.create_all(connection.engine)
