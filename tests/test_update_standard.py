from standard import Standard

def test_add_new_chars_to_standard():
    standard = Standard(case_sensitive=True, charset={"a": "A", "b": "B", "c": "C"})
    standard.create()
    standard.update_charset(codepoints={"d": "D", "e": "E", "f": "F"})

def test_update_standard_by_overriding_some_chars():
    standard = Standard(charset={"a": "A", "b": "B", "c": "x"})
    standard.create()
    standard.update_charset(codepoints={"c": "c", "d": "D", "e": "e"})

def test_update_not_existing_standard():
    standard = Standard()
    standard.update_charset(codepoints={"x": "!"}, expected_status_code=404)

def test_add_encoded_char_len_not_matching_to_standard():
    standard = Standard(encoded_char_len=1)
    standard.create()
    standard.update_charset(codepoints={"a": "ax"}, expected_status_code=422)

def test_add_char_with_len_different_than_1_to_standard():
    standard = Standard()
    standard.create()
    standard.update_charset(codepoints={"az": "x"}, expected_status_code=422)

def test_add_empty_encoded_char_to_standard():
    standard = Standard()
    standard.create()
    standard.update_charset(codepoints={"x": ""}, expected_status_code=422)

def test_add_non_unique_encoded_char_to_standard():
    standard = Standard(charset={"a": "A", "b": "B", "c": "C"})
    standard.create()
    standard.update_charset(codepoints={"d": "C"}, expected_status_code=422)

def test_update_standard_with_encoded_char_containing_encoded_char_sep():
    standard = Standard(encoded_char_sep="/")
    standard.create()
    standard.update_charset(codepoints={"a": "c/x"}, expected_status_code=422)
