# main.py

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from parser import load_and_validate
from calc import analyze_primers
from dimers import self_complementarity, dimer_check
from report import save_csv, plot_gc_tm_multi, plot_flags_multi


def run_dimer_analysis(valid_primers):
    names = list(valid_primers.keys())
    sequences = list(valid_primers.values())
    dimer_results = {}

    for i, (name, seq) in enumerate(zip(names, sequences)):
        self_comp = self_complementarity(seq)
        has_dimer = False
        for j, seq2 in enumerate(sequences):
            if i != j and dimer_check(seq, seq2):
                has_dimer = True
                break
        dimer_results[name] = {
            'self_complementarity': self_comp,
            'dimer': has_dimer
        }
    return dimer_results


def process_file(filepath):
    """
    Parses, validates and analyses a single FASTA/CSV file.
    Returns list of result dicts.
    """
    valid_primers, errors = load_and_validate(filepath)

    if errors:
        print(f"  Skipped {len(errors)} invalid sequences")

    if not valid_primers:
        print(f"  No valid primers found in {filepath}, skipping.")
        return []

    print(f"  Loaded {len(valid_primers)} valid primers")

    calc_results = analyze_primers(valid_primers)
    dimer_results = run_dimer_analysis(valid_primers)

    final_results = []
    for r in calc_results:
        if not r.get('valid', True):
            continue
        name = r['name']
        final_results.append({
            'name': name,
            'sequence': r['sequence'],
            'length': r['length'],
            'tm_wallace': r['tm_wallace'],
            'gc_content': r['gc_content'],
            'gc_ok': not r['gc_out_of_range'],
            'length_ok': not r['length_out_of_range'],
            'self_complementarity': dimer_results[name]['self_complementarity'],
            'dimer': dimer_results[name]['dimer']
        })

    return final_results


def main():
    arg_parser = argparse.ArgumentParser(
        description="PCRpal - Batch validation and analysis of PCR primers."
    )
    arg_parser.add_argument(
        "input",
        nargs='+',  # accepts one or more files
        help="Path(s) to input file(s) (.csv or .fasta/.fa)"
    )
    arg_parser.add_argument(
        "-o", "--output",
        help="Output directory for reports and plots (default: output/)",
        default="output"
    )
    arg_parser.add_argument(
        "--plots",
        help="Generate matplotlib plots",
        action="store_true"
    )

    args = arg_parser.parse_args()
    os.makedirs(args.output, exist_ok=True)

    print("--- PCRpal ---")

    # process each file separately
    all_results = {}  # {filename: [list of result dicts]}

    for filepath in args.input:
        if not os.path.exists(filepath):
            print(f"Warning: File '{filepath}' not found, skipping.")
            continue

        label = os.path.splitext(os.path.basename(filepath))[0]
        print(f"\nProcessing: {filepath}")

        results = process_file(filepath)
        if results:
            all_results[label] = results

            # save individual CSV per file
            csv_path = os.path.join(args.output, f"{label}_report.csv")
            save_csv(results, csv_path)

    if not all_results:
        print("\nNo valid data found. Aborting.")
        sys.exit(1)

    # generate comparison plots if --plots flag is set
    if args.plots:
        print("\nGenerating comparison plots...")
        plot_gc_tm_multi(all_results, os.path.join(args.output, "gc_vs_tm.png"))
        plot_flags_multi(all_results, os.path.join(args.output, "flags_summary.png"))

    print(f"\nDone! Results saved to: {args.output}/")


if __name__ == "__main__":
    main()