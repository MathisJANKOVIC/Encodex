from standard import Standard

def test_get_all_standards():
    Standard.get_all()

def test_get_all_standards_and_if_created_standards_are_in_it():
    standard1 = Standard()
    standard1.create()

    standard2 = Standard()
    standard2.create()

    standards = [standard for standard in Standard.get_all() if standard["name"] == standard1.name or standard["name"] == standard2.name]
    assert len(standards) == 2, "expected to find 2 standards with the names of the created ones, got " + str(len(standards))

    assert standards[0] == standard1.__dict__, "created standard not found in the list of all standards"
    assert standards[1] == standard2.__dict__, "created standard not found in the list of all standards"

def test_get_standard():
    standard = Standard()
    standard.create()
    standard.get()

def test_get_non_existent_standard():
    standard = Standard()
    standard.get(expected_status_code=404)
