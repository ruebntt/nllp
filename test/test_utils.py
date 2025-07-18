from app.utils import parse_array_from_str, array_to_str

def test_parse_array_from_str():
    assert parse_array_from_str("3,2,1") == [3, 2, 1]
    assert parse_array_from_str("10,20") == [10, 20]

def test_array_to_str():
    assert array_to_str([3, 2, 1]) == "3,2,1"
    assert array_to_str([]) == ""
