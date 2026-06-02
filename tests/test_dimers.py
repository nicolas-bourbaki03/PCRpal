# tests/test_dimers.py
import sys
sys.path.append('scripts')

from dimers import reverse_complement, self_complementarity, dimer_check

# test on real primers from data/ file
primer_f = "CCTCTGCGGTGCCAAGCCTC"   # L18749.1 forward exon 8
primer_r = "CGTGGTGGTCCCGGCCGCC"    # L18748.1 reverse exon 7

print("=== Test dimers.py ===")
print(f"Primer F: {primer_f}")
print(f"Primer R: {primer_r}")
print(f"Reverse complement of F: {reverse_complement(primer_f)}")
print(f"Self-complementarity F: {self_complementarity(primer_f)}")
print(f"Self-complementarity R: {self_complementarity(primer_r)}")
print(f"Dimer check F+R: {dimer_check(primer_f, primer_r)}")