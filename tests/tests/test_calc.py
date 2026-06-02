from scripts.calc import (
    clean_sequence,
    is_valid_dna,
    primer_length,
    tm_wallace,
    gc_content,
    is_gc_out_of_range,
    is_length_out_of_range,
    analyze_primer,
)


def test_clean_sequence():
    assert clean_sequence(" atgc\n") == "ATGC"


def test_is_valid_dna_valid_sequence():
    assert is_valid_dna("ATGCATGC") is True


def test_is_valid_dna_invalid_sequence():
    assert is_valid_dna("ATGCNN") is False


def test_primer_length():
    assert primer_length("ATGCATGC") == 8


def test_tm_wallace():
    assert tm_wallace("ATGC") == 12


def test_gc_content():
    assert gc_content("ATGC") == 50.0


def test_gc_out_of_range_high_gc():
    assert is_gc_out_of_range("GCGCGCGC") is True


def test_gc_out_of_range_normal_gc():
    assert is_gc_out_of_range("ATGCATGC") is False


def test_length_out_of_range_short_primer():
    assert is_length_out_of_range("ATGC") is True


def test_length_out_of_range_normal_primer():
    assert is_length_out_of_range("ATGCATGCATGCATGCATGC") is False


def test_analyze_primer_valid():
    result = analyze_primer("test_primer", "ATGCATGCATGCATGCATGC")

    assert result["name"] == "test_primer"
    assert result["length"] == 20
    assert result["valid"] is True
    assert result["error"] == ""


def test_analyze_primer_invalid():
    result = analyze_primer("bad_primer", "ATGCNNNN")

    assert result["valid"] is False
    assert result["error"] == "Invalid sequence: only A, T, G, C are allowed"
