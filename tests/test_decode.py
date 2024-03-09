from standard import Standard

def test_decode_using_maj_standard():
    standard = Standard.new_maj()
    standard.create()
    decoded_str = standard.decode("TEST")
    assert decoded_str == "test", Standard.wrong_decoded_str_message(decoded_str, "test")

def test_decode_using_maj_standard_with_unreferenced_char():
    standard = Standard.new_maj()
    standard.create()
    decoded_str = standard.decode("TEST !")
    assert decoded_str == "test !", Standard.wrong_decoded_str_message(decoded_str, "test !")

def test_decode_using_morse_standard():
    standard = Standard.new_morse()
    standard.create()
    decoded_str = standard.decode("- .... .. ... / .. ... / .- / - . ... -")
    assert decoded_str == "this is a test", Standard.wrong_decoded_str_message(decoded_str, "this is a test")

def test_decode_using_morse_standard_with_unreferenced_char():
    standard = Standard.new_morse()
    standard.create()
    standard.decode("/Novak Djokovic is the GOAT/", expected_status_code=422)

def test_decode_using_non_existent_standard():
    standard = Standard.new_morse()
    standard.decode("azerty", expected_status_code=404)
