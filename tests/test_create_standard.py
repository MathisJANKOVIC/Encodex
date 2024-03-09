from standard import Standard

def test_create_standard_with_defined_encoded_char_len_and_empty_sep():
    standard = Standard(
        case_sensitive = True,
        allowed_unrefenced_chars = True,
        encoded_char_len = 1,
        encoded_char_sep = "",
        charset = {"a": "A", "b": "B", "c": "C"}
    )
    standard.create(expected_status_code=201)

def test_create_standard_with_encoded_char_sep_and_undefined_len():
    standard = Standard(
        case_sensitive = False,
        allowed_unrefenced_chars = False,
        encoded_char_len = None,
        encoded_char_sep = "-",
        charset = {"a": "z", "b": "yy", "c": "xxx"}
    )
    standard.create(expected_status_code=201)

def test_create_duplicate_standard():
    standard = Standard()
    standard.create()
    standard.create(expected_status_code=409)

def test_create_standard_with_too_short_name():
    standard = Standard("ax")
    standard.create(expected_status_code=422)

def test_create_standard_with_too_long_name():
    standard = Standard("w" * 37)
    standard.create(expected_status_code=422)

def test_create_standard_with_special_char_in_name():
    standard = Standard("#standard")
    standard.create(expected_status_code=422)

def test_create_standard_with_encoded_char_len_small_than_1():
    standard = Standard(encoded_char_len=0)
    standard.create(expected_status_code=422)

def test_create_standard_with_undefined_encoded_char_len_and_empty_sep():
    standard = Standard(encoded_char_sep="", encoded_char_len=None)
    standard.create(expected_status_code=422)

def test_create_standard_with_undefined_encoded_char_len_and_empty_encoded_char():
    standard = Standard(charset={"a": ""}, encoded_char_len=None)
    standard.create(expected_status_code=422)

def test_create_standard_with_encoded_char_len_not_matching():
    standard = Standard(charset={"a": "rs"}, encoded_char_len=1)
    standard.create(expected_status_code=422)

def test_create_standard_with_encoded_char_sep_in_encoded_char():
    standard = Standard(charset={"a": "f/x"}, encoded_char_sep="/")
    standard.create(expected_status_code=422)