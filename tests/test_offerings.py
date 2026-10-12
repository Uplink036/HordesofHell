from data.offerings import load_offerings, is_offering

def test_load_offerings():
    offerings = load_offerings()
    assert isinstance(offerings, list)
    assert all(isinstance(offering, str) for offering in offerings)

def test_is_offering_with_real_offering():
    assert is_offering("The Ambushing Hellborne") is True

def test_is_offering_with_non_existing_offering():
    assert is_offering("non_existing_offering") is False

def test_is_offering_with_all_offerings():
    offerings = load_offerings()
    for offering in offerings:
        assert is_offering(offering) is True