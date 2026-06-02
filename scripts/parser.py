import csv
import os

def validate_sequence(seq, min_length=15):
    seq = seq.upper().strip()
    
    if len(seq) < min_length:
        return False, seq, f"Too short (min {min_length} bp)"
    
    allowed_chars = set("ATGC")
    if not set(seq).issubset(allowed_chars):
        return False, seq, "Contains invalid characters (only ATGC allowed)"
        
    return True, seq, "OK"

def parse_csv(filepath):
    primers = {}
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                name, seq = row[0].strip(), row[1].strip()
                primers[name] = seq
    return primers

def parse_fasta(filepath):
    primers = {}
    with open(filepath, mode='r', encoding='utf-8') as f:
        name = ""
        seq_parts = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name:
                    primers[name] = "".join(seq_parts)
                name = line[1:]
                seq_parts = []
            else:
                seq_parts.append(line)
        if name:
            primers[name] = "".join(seq_parts)
    return primers

def load_and_validate(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.csv':
        raw_primers = parse_csv(filepath)
    elif ext in ['.fasta', '.fa']:
        raw_primers = parse_fasta(filepath)
    else:
        raise ValueError(f"Unsupported format: {ext}. Use .csv or .fasta")

    valid_primers = {}
    errors = {}

    for name, seq in raw_primers.items():
        is_valid, clean_seq, msg = validate_sequence(seq)
        if is_valid:
            valid_primers[name] = clean_seq
        else:
            errors[name] = msg

    return valid_primers, errors