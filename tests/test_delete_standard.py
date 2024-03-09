from standard import Standard

def test_delete_standard():
    standard = Standard(charset={"a": "b"})
    standard.create()
    standard.delete()

def test_delete_not_existing_standard():
    standard = Standard()
    standard.delete(expected_status_code=404)
