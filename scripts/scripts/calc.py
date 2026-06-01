def clean_sequence(sequence):
    return sequence.replace(" ", "").replace("\n", "").replace("\r", "").upper()


def is_valid_dna(sequence):
    sequence = clean_sequence(sequence)

    if len(sequence) == 0:
        return False

    allowed_bases = {"A", "T", "G", "C"}

    for base in sequence:
        if base not in allowed_bases:
            return False

    return True


def primer_length(sequence):
    return len(clean_sequence(sequence))


def tm_wallace(sequence):
    sequence = clean_sequence(sequence)

    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")

    return 2 * (a_count + t_count) + 4 * (g_count + c_count)


def gc_content(sequence):
    sequence = clean_sequence(sequence)

    if len(sequence) == 0:
        return 0.0

    g_count = sequence.count("G")
    c_count = sequence.count("C")

    return round(((g_count + c_count) / len(sequence)) * 100, 2)


def is_gc_out_of_range(sequence, min_gc=40, max_gc=60):
    gc = gc_content(sequence)
    return gc < min_gc or gc > max_gc


def is_length_out_of_range(sequence, min_len=18, max_len=25):
    length = primer_length(sequence)
    return length < min_len or length > max_len


def analyze_primer(name, sequence):
    sequence = clean_sequence(sequence)

    if not is_valid_dna(sequence):
        return {
            "name": name,
            "sequence": sequence,
            "length": "",
            "tm_wallace": "",
            "gc_content": "",
            "gc_out_of_range": "",
            "length_out_of_range": "",
            "valid": False,
            "error": "Invalid sequence: only A, T, G, C are allowed"
        }

    return {
        "name": name,
        "sequence": sequence,
        "length": primer_length(sequence),
        "tm_wallace": tm_wallace(sequence),
        "gc_content": gc_content(sequence),
        "gc_out_of_range": is_gc_out_of_range(sequence),
        "length_out_of_range": is_length_out_of_range(sequence),
        "valid": True,
        "error": ""
    }


def analyze_primers(primers):
    results = []

    for name, sequence in primers.items():
        results.append(analyze_primer(name, sequence))

    return results
