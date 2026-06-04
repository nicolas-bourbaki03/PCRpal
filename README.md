# PCRpal

**Python CLI tool for batch validation and analysis of PCR primers**

> Maria Szczerbińska - team leader [nicolas-bourbaki03](https://github.com/nicolas-bourbaki03), Agata Dubińska [Agatadubinska](https://github.com/Agatadubinska), Katarzyna Makowska [kmakowska22-glitch](https://github.com/kmakowska22-glitch)
>
> Architecture of Large Projects in Bioinformatics, 2026 | Master Studies in Bioinformatics at University of Warsaw

---

## Motivation

PCR primer design is one of the most common steps in molecular biology workflows.
Existing tools such as Primer3 and OligoCalc require manual input of sequences
one by one. PCRpal allows batch validation of multiple primers at once from a
single input file, saving time and reducing human error.

---

## Features

- Melting temperature (Tm) calculation - Wallace rule
- GC content calculation with out-of-range flagging (optimal: 40–60%)
- Sequence length validation (optimal: 18–25 bp)
- Input sequence validation (only ATGC allowed)
- Self-complementarity check (hairpin detection)
- Primer dimer detection (forward + reverse pair check)
- CSV report generation
- Data visualization (scatter plot Tm vs GC, bar chart of flags)

## Project Structure

```
PCRpal/
├── README.md
├── LICENSE
├── requirements.txt
├── scripts/
│   ├── main.py         # orchestrates the pipeline, CLI interface
│   ├── parser.py       # input file reading and validation (FASTA, CSV)
│   ├── calc.py         # Tm, GC content, length calculations
│   ├── dimers.py       # self-complementarity and dimer check
│   └── report.py       # CSV report and plots
├── tests/
│   └── test_dimers.py  # unit tests for dimers module
├── data/
│   ├── sequence.fasta
│   ├── sequence_homo_sapiens.fasta
│   ├── sequence_bacterial.fasta
│   ├── sequence_viral.fasta
│   └── sequence_SRT_marker.fasta
└── output/             # generated reports and plots
```

## Tasks

### Main tasks
- [x] Input parser (FASTA + CSV)
- [x] Tm calculation (Wallace rule)
- [x] GC content + length validation
- [x] Self-complementarity check
- [x] Primer dimer detection
- [x] CSV report export
- [x] Matplotlib visualizations
- [x] Multi-dataset comparison mode
- [x] Project repository setup (README, licence, structure)

---

## Installation

```bash
git clone https://github.com/nicolas-bourbaki03/PCRpal.git
cd PCRpal
pip install -r requirements.txt
```

---

## Usage

```bash
# single file
python scripts/main.py data/sequence.fasta

# single file with plots
python scripts/main.py data/sequence.fasta --plots

# multiple files - comparison mode
python scripts/main.py data/file1.fasta data/file2.fasta data/file3.fasta --plots

# custom output directory
python scripts/main.py data/sequence.fasta --plots -o results/
```

Each input file gets its own CSV report. Plots compare all datasets:
- `gc_vs_tm.png` - scatter plot of Tm vs GC content, one color per dataset
- `flags_summary.png`- bar chart of flagged primer percentages per dataset

---

## Input Format

PCRpal accepts **FASTA** or **CSV** files.

**FASTA example:**
```
>primer_forward
ATGCATGCATGCATGC
>primer_reverse
GCTAGCTAGCTAGCTA
```
```
**CSV example:**
name,sequence
primer_forward,ATGCATGCATGCATGC
primer_reverse,GCTAGCTAGCTAGCTA
```
---

## Modules

### `main.py`
Orchestrates the full pipeline. Accepts one or more FASTA/CSV files via CLI,
runs parsing, analysis, dimer checks, and generates reports and plots.

### `parser.py`
Reads FASTA and CSV input files. Validates each sequence - checks for invalid
characters and minimum length (15 bp). Returns a dictionary of valid primers
and a separate dictionary of errors.

### `calc.py`
Calculates primer properties: melting temperature (Tm) using the Wallace rule
`2*(A+T) + 4*(G+C)`, GC content (%), sequence length, and out-of-range flags
for GC content (40–60%) and length (18–25 bp).

### `dimers.py`
Checks for self-complementarity (hairpin formation) and primer dimer risk
by comparing sequences with their reverse complements using a sliding window
approach (default: minimum 4-base match).

### `report.py`
Generates a CSV summary report and matplotlib visualizations:
scatter plot of Tm vs GC content, and a bar chart of flagged issues per primer.

---

## Dependencies

- `matplotlib`
- `numpy`

```bash
pip install -r requirements.txt
```

---

## References

- Untergasser et al. (2012) - Primer3: https://doi.org/10.1093/nar/gks596  
- Kibbe (2007) - OligoCalc: https://doi.org/10.1093/nar/gkm234