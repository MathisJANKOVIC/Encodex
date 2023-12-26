from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.models import EncodingStandard
from database.connection import LocalSession

class CreateEncodingStandard(BaseModel):
    name: str = Field(...,
        description = "Name of the encoding standard",
        example = "ASCII-hexa"
    )
    case_sensitive: bool = Field(...,
        description = "Whether the encoding standard is case sensitive or not, if true, 'a' and 'A' will be treated as different characters",
        example = True
    )
    allowed_unrefenced_chars: bool = Field(...,
        description = "Behavior when a character is not defined in the encoding standard while encoding or decoding. If true, the character will be kept, if false, an exception will be raised",
        example = False
    )
    encoded_char_len: int | None = Field(None,
        description = "Length of all encoded characters. If null, encoded characters won't have a fixed length.",
        example = 2
    )
    encoded_char_sep: str = Field(...,
        description = "Separator of the encoded characters. Can be empty only if 'encoded_char_len' is defined.",
        example = " "
    )
    charset: dict[str, str] = Field(...,
        description = "Dictionary mapping characters to their encoded representations in the encoding standard",
        example = {
            "!": "21", "$": "24", "%": "25", "&": "26", "'": "27", "(": "28", ")": "29", "*": "2A", ",": "2C", "-": "2D", "{": "7B", "}": "7D", ":": "3A",
            ".": "2E", "/": "2F", "0": "30", "1": "31", "2": "32", "3": "33", "4": "34", "5": "35", "6": "36", "7": "37", "8": "38", "9": "39", " ": "20",
            ";": "3B", "<": "3C", "=": "3D", ">": "3E", "?": "3F", "@": "40", "A": "41", "B": "42", "C": "43", "D": "44", "E": "45", "F": "46", "G": "47",
            "H": "48", "I": "49", "J": "4A", "K": "4B", "L": "4C", "M": "4D", "N": "4E", "O": "4F", "P": "50", "Q": "51", "R": "52", "S": "53","T": "54",
            "U": "55", "V": "56", "W": "57", "X": "58", "Y": "59", "Z": "5A", "[": "5B", "\\": "5C", "]": "5D", "^": "5E", "_": "5F", "`": "60", "a": "61",
            "b": "62", "c": "63", "d": "64", "e": "65", "f": "66", "g": "67", "h": "68", "i": "69", "j": "6A", "k": "6B", "l": "6C", "m": "6D","n": "6E",
            "o": "6F", "p": "70", "q": "71", "r": "72", "s": "73", "t": "74", "u": "75", "v": "76", "w": "77", "x": "78", "y": "79", "z": "7A", "#": "23",
        }
    )

router = APIRouter()

@router.post("/encodex/create/")
def create_encoding_standard(encoding_standard: CreateEncodingStandard = Body(...)):

    with LocalSession() as session:
        try:
            if(session.query(EncodingStandard).filter(EncodingStandard.name == encoding_standard.name).first() is not None):
                raise HTTPException(status_code=409, detail=f"Encoding standard '{encoding_standard.name}' already exists")

            if(len(encoding_standard.name) < 3):
                raise HTTPException(status_code=422, detail="Encoding standard name cannot have less than 3 characters")

            if(len(encoding_standard.name) > 32):
                raise HTTPException(status_code=422, detail="Encoding standard name cannot have more than 32 characters")

            if(not encoding_standard.name.replace(" ","").replace("-","").replace("_","").isalnum()):
                raise HTTPException(status_code=422, detail="Encoding standard name cannot contain special characters")

            if(len(encoding_standard.charset.values()) != len(set(encoding_standard.charset.values()))):
                raise HTTPException(status_code=422, detail="Encoded characters must be unique")

            if(encoding_standard.encoded_char_len is None and encoding_standard.encoded_char_sep == ""):
                raise HTTPException(status_code=422, detail="encoded_char_len and encoded_char_sep cannot be both undefined or empty for an encoding standard")

            if(not encoding_standard.case_sensitive):
                encoding_standard.charset = {char.lower(): encoded_char for char, encoded_char in encoding_standard.charset.items()}

            for char, encoded_char in encoding_standard.charset.items():
                if(len(char) != 1):
                    raise HTTPException(status_code=422, detail="Characters must be one character long")

                if(encoding_standard.encoded_char_len is None):
                    if(encoded_char == ""):
                        raise HTTPException(status_code=422, detail="Encoded characters cannot be empty")
                elif(len(encoded_char) != encoding_standard.encoded_char_len):
                    raise HTTPException(status_code=422, detail="Encoded characters lenght must be the same as defined in encoding standard")

                if(encoding_standard.encoded_char_sep != "" and encoding_standard.encoded_char_sep in encoded_char):
                    raise HTTPException(status_code=422, detail="Encoded characters cannot contain character separator")

            session.add(EncodingStandard(
                name = encoding_standard.name,
                case_sensitive = encoding_standard.case_sensitive,
                allowed_unrefenced_chars = encoding_standard.allowed_unrefenced_chars,
                encoded_char_len = encoding_standard.encoded_char_len,
                encoded_char_sep = encoding_standard.encoded_char_sep,
                charset = encoding_standard.charset
            ))
            session.commit()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An unexpected error has occured with the database")

    return JSONResponse(status_code=201, content={"detail": f"Encoding standard '{encoding_standard.name}' created successfully"})