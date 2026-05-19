# dimers.py

def reverse_complement(seq):
    """
    Returns reverse complement of a DNA sequence.
    E.g. ATGC -> GCAT
    """
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement[base] for base in reversed(seq.upper()))


def self_complementarity(seq, min_match=4):
    """
    Checks if primer can form hairpin with itself.
    Compares primer with its own reverse complement using sliding window.
    Returns True if problematic (found match >= min_match bases).
    """
    seq = seq.upper()
    rev_comp = reverse_complement(seq)
    
    for i in range(len(seq) - min_match + 1):
        window = seq[i:i + min_match]
        if window in rev_comp:
            return True
    return False


def dimer_check(seq1, seq2, min_match=4):
    """
    Checks if two primers can bind to each other (primer dimer).
    Compares seq1 with reverse complement of seq2.
    Returns True if problematic (found match >= min_match bases).
    """
    seq1 = seq1.upper()
    rev_comp_seq2 = reverse_complement(seq2)
    
    for i in range(len(seq1) - min_match + 1):
        window = seq1[i:i + min_match]
        if window in rev_comp_seq2:
            return True
    return False


# quick test - mozna usunac pozniej
if __name__ == "__main__":
    primer_f = "ATGCATGCATGC"
    primer_r = "GCTAGCTAGCTA"
    
    print("Reverse complement:", reverse_complement(primer_f))
    print("Self-complementarity:", self_complementarity(primer_f))
    print("Dimer check:", dimer_check(primer_f, primer_r))