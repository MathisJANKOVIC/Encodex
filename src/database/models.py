from __future__ import annotations
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship, declarative_base

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
    allowed_unrefenced_chars = Column(Boolean)

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

        for char, encoded_char in charset.items():
            self.charset.append(CodePoint(char, encoded_char))

    def dict(self) -> dict:
        """Returns a dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "case_sensitive": self.case_sensitive,
            "allowed_unrefenced_chars": self.allowed_unrefenced_chars,
            "encoded_char_len": self.encoded_char_len,
            "encoded_char_sep": self.encoded_char_sep,
            "charset": {encoding_char.char: encoding_char.encoded_char for encoding_char in self.charset}
        }

    def encode(self, char: str) -> str | None:
        """Returns the encoded string of `char` if exists in the charset otherwise returns None"""
        for code_point in self.charset:
            if(code_point.char == char):
                return code_point.encoded_char
        return None

    def decode(self, encoded_char: str) -> str | None:
        """Returns the decoded string of `encoded_char` if exists in the charset otherwise returns None"""
        for code_point in self.charset:
            if(code_point.encoded_char == encoded_char):
                return code_point.char
        return None

    def delete(self, session: Session):
        """Deletes the encoding standard"""
        session.query(CodePoint).filter(CodePoint.encoding_standard_id == self.id).delete()
        session.delete(self)

    def is_encoded_char_used_by_another_char(self, char: str, encoded_char: str) -> bool:
        """Returns True if `encoded_char` is taken by another character in the charset otherwise returns False"""
        for code_point in self.charset:
            if(code_point.char != char and code_point.encoded_char == encoded_char):
                return True
        return False

    def get_code_point(self, char: str) -> CodePoint | None:
        """Returns `CodePoint` with the given `char` if exists in the charset otherwise returns None"""
        for code_point in self.charset:
            if(code_point.char == char):
                return code_point

    @staticmethod
    def get(session: Session, id: int = None, name: str = None) -> EncodingStandard | None:
        """Returns `EncodingStandard` with the given `id` and `name` if exists otherwise returns None"""
        if(id and name):
            return session.query(EncodingStandard).filter(EncodingStandard.id == id).filter(EncodingStandard.name == name).first()
        elif(id):
            return session.query(EncodingStandard).filter(EncodingStandard.id == id).first()
        elif(name):
            return session.query(EncodingStandard).filter(EncodingStandard.name == name).first()
        else:
            return session.query(EncodingStandard).all()


if(__name__ == '__main__'):
    Base.metadata.drop_all(connection.engine)
    Base.metadata.create_all(connection.engine)
