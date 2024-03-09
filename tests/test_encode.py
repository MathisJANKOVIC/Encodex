from standard import Standard

def test_encode_using_to_maj_standard():
    standard = Standard.new_maj()
    standard.create()
    encoded_str = standard.encode("test")
    assert encoded_str == "TEST", Standard.wrong_encoded_str_message(encoded_str, "TEST")


def test_encode_using_to_maj_standard_with_unreferenced_char():
    standard = Standard.new_maj()
    standard.create()
    encoded_str = standard.encode("test !")
    assert encoded_str == "TEST !", Standard.wrong_encoded_str_message(encoded_str, "TEST !")

def test_encode_using_morse_standard():
    standard = Standard.new_morse()
    standard.create()
    encoded_str = standard.encode("this is a test")
    assert encoded_str == "- .... .. ... / .. ... / .- / - . ... -", Standard.wrong_encoded_str_message(encoded_str, "- .... .. ... / .. ... / .- / - . ... -")

def test_encode_using_morse_standard_with_unreferenced_char():
    standard = Standard.new_morse()
    standard.create()
    standard.encode("/Novak Djokovic is the GOAT/", expected_status_code=422)

def test_encode_using_morse_standard_sending_uppercase_chars():
    standard = Standard.new_morse()
    standard.create()
    encoded_str = standard.encode("SOS")
    assert encoded_str == "... --- ...", Standard.wrong_encoded_str_message(encoded_str, "... --- ...")

def test_encode_using_non_existent_standard():
    standard = Standard.new_morse()
    standard.encode("azerty", expected_status_code=404)
