from apps.demo_yapf import count_words, normalize_name, parse_int_list


def test_normalize_name():
    assert normalize_name("  nguyen   van   a ") == "Nguyen Van A"


def test_count_words():
    freq = count_words("Hello hello world!")
    assert freq["hello"] == 2
    assert freq["world"] == 1


def test_parse_int_list():
    assert parse_int_list("1, 2,3") == [1, 2, 3]
    assert parse_int_list("") == []
