# analysis
def calculate_tm_wallace(sequence: str) -> int:
    sequence = sequence.upper()

    a = sequence.count("A")
    t = sequence.count("T")
    g = sequence.count("G")
    c = sequence.count("C")

    return 2 * (a + t) + 4 * (g + c)


def calculate_gc_content(sequence: str) -> float:
    sequence = sequence.upper()

    if len(sequence) == 0:
        return 0.0

    g = sequence.count("G")
    c = sequence.count("C")

    return ((g + c) / len(sequence)) * 100


def get_length(sequence: str) -> int:
    return len(sequence)


def is_gc_in_range(sequence: str) -> bool:
    gc = calculate_gc_content(sequence)
    return 40 <= gc <= 60


def is_length_in_range(sequence: str) -> bool:
    length = get_length(sequence)
    return 18 <= length <= 25


def validate_sequence(sequence: str) -> bool:
    sequence = sequence.upper()
    allowed_letters = set("ATGC")

    for letter in sequence:
        if letter not in allowed_letters:
            return False

    return True


def analyze_primer(sequence: str) -> dict:
    sequence = sequence.upper()

    if not validate_sequence(sequence):
        return {
            "sequence": sequence,
            "error": "Invalid sequence - only A, T, G, C are allowed"
        }

    return {
        "sequence": sequence,
        "length": get_length(sequence),
        "tm_wallace": calculate_tm_wallace(sequence),
        "gc_content": round(calculate_gc_content(sequence), 2),
        "gc_ok": is_gc_in_range(sequence),
        "length_ok": is_length_in_range(sequence),
    }


if __name__ == "__main__":
    test_primers = [
        "ATGCGTACGTAGCTAGCTA",
        "ATATATATATATATATATA",
        "GCGCGCGCGCGCGCGCGCGC",
        "ATGC",
        "ATGCGTACGTAGCTAGCTAGCTAGCTA",
        "ATGCBLA"
    ]

    for primer in test_primers:
        result = analyze_primer(primer)
        print(result)