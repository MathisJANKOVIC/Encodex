from standard import Standard

def test_rename_standard():
    standard = Standard()
    standard.create()
    standard.rename()

def test_rename_standard_with_existing_name():
    standard = Standard()
    standard.create()

    standard2 = Standard()
    standard2.create()

    standard.rename(new_name=standard2.name, expected_status_code=409)

def test_rename_non_existing_standard():
    standard = Standard()
    standard.rename(expected_status_code=404)