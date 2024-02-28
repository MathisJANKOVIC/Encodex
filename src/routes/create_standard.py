from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field

from database.models import EncodingStandard
from database.connection import LocalSession

class CreateEncodingStandard(BaseModel):
    name: str = Field(...,
        example = "ASCII-hexa",
        description = "Name of the encoding standard."
    )
    case_sensitive: bool = Field(...,
        example = True,
        description = """Whether the encoding standard is case sensitive or not.
        If true, 'a' and 'A' will be treated as different characters."""
    )
    allowed_unrefenced_chars: bool = Field(...,
        example = False,
        description = """Behavior when a character is not defined in the encoding standard while encoding or decoding.
        If true, the character will be kept, if false, the API will return an error."""
    )
    encoded_char_len: int | None = Field(None,
        example = 2,
        description = "Length of all encoded characters. If null, encoded characters won't have a fixed length."
    )
    encoded_char_sep: str = Field(...,
        example = " ",
        description = "Separator of the encoded characters, can be empty only if 'encoded_char_len' is defined."
    )
    charset: dict[str, str] = Field(...,
        description = "Dictionary mapping characters to their encoded representations in the encoding standard.",
        example = {
            "!": "21", "$": "24", "%": "25", "&": "26", "'": "27", "(": "28", ")": "29", "*": "2A", ",": "2C",
            "-": "2D", "{": "7B", "}": "7D", ":": "3A", ".": "2E", "/": "2F", "0": "30", "1": "31", "2": "32",
            "3": "33", "4": "34", "5": "35", "6": "36", "7": "37", "8": "38", "9": "39", " ": "20", ";": "3B",
            "<": "3C", "=": "3D", ">": "3E", "?": "3F", "@": "40", "A": "41", "B": "42", "C": "43", "D": "44",
            "E": "45", "F": "46", "G": "47", "H": "48", "I": "49", "J": "4A", "K": "4B", "L": "4C", "M": "4D",
            "N": "4E", "O": "4F", "P": "50", "Q": "51", "R": "52", "S": "53","T": "54", "U": "55", "V": "56",
            "W": "57", "X": "58", "Y": "59", "Z": "5A", "[": "5B", "\\": "5C", "]": "5D", "^": "5E", "_": "5F",
            "`": "60", "a": "61", "b": "62", "c": "63", "d": "64", "e": "65", "f": "66", "g": "67", "h": "68",
            "i": "69", "j": "6A", "k": "6B", "l": "6C", "m": "6D","n": "6E", "o": "6F", "p": "70", "q": "71",
            "r": "72", "s": "73", "t": "74", "u": "75", "v": "76", "w": "77", "x": "78", "y": "79", "z": "7A",
        }
    )

router = APIRouter()

@router.post("/encoding-standard/create")
def create_encoding_standard(standard: CreateEncodingStandard = Body(...)):

    with LocalSession() as session:
        try:
            if(EncodingStandard.get(session, name=standard.name) is not None):
                raise HTTPException(status_code=409, detail="An encoding standard with this name already exists")

            if(len(standard.name) < 3):
                raise HTTPException(status_code=422, detail="encoding_standard_name cannot have less than 3 characters")

            if(len(standard.name) > 36):
                raise HTTPException(status_code=422, detail="encoding_standard_name cannot have more than 36 characters")

            if(not standard.name.replace(" ","").replace("-","").replace("_","").isalnum()):
                raise HTTPException(status_code=422, detail="encoding_standard_name cannot contain special characters")

            if(len(standard.charset.values()) != len(set(standard.charset.values()))):
                raise HTTPException(status_code=422, detail="Encoded characters in charset must be unique")

            if(standard.encoded_char_len is not None and standard.encoded_char_len < 1):
                raise HTTPException(status_code=422, detail="encoded_char_len must be greater than 0")

            if(standard.encoded_char_len is None and standard.encoded_char_sep == ""):
                raise HTTPException(
                    status_code = 422,
                    detail = "encoded_char_sep cannot be empty without a defined encoded_char_len"
                )

            if(not standard.case_sensitive):
                standard.charset = {char.lower(): encoded_char for char, encoded_char in standard.charset.items()}

            for char, encoded_char in standard.charset.items():
                if(len(char) != 1):
                    raise HTTPException(status_code=422, detail="Characters in charset must be one character long")

                if(encoded_char == ""):
                    raise HTTPException(status_code=422, detail="Encoded characters in charset cannot be empty")

                if(len(encoded_char) != standard.encoded_char_len and standard.encoded_char_len is not None):
                    raise HTTPException(
                        status_code = 422,
                        detail = "Encoded characters in charset must have the same length as encoded_char_len"
                    )

                if(standard.encoded_char_sep in encoded_char and standard.encoded_char_sep != ""):
                    raise HTTPException(status_code=422, detail="Encoded characters in charset cannot contain encoded_char_sep")

            new_standard = EncodingStandard(
                name = standard.name.strip(),
                case_sensitive = standard.case_sensitive,
                allowed_unrefenced_chars = standard.allowed_unrefenced_chars,
                encoded_char_len = standard.encoded_char_len,
                encoded_char_sep = standard.encoded_char_sep,
                charset = standard.charset
            )

            session.add(new_standard)
            session.commit()

            new_standard_dict = new_standard.dict()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=201, content={"encoding_standard": new_standard_dict, "detail": "Encoding standard created successfully"})