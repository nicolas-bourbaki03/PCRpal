import argparse
import sys
from parser import load_and_validate

def main():
    parser = argparse.ArgumentParser(
        description="PCRpal - Batch validation and analysis of PCR primers."
    )
    parser.add_argument(
        "input", 
        help="Path to the input file with primers (.csv or .fasta)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to the report file (.csv)", 
        default="pcrpal_report.csv"
    )
    
    args = parser.parse_args()

    print(f"Loading primers from file: {args.input}...")
    
    try:
        valid_primers, errors = load_and_validate(args.input)
    except FileNotFoundError:
        print(f"Error: File {args.input} does not exist.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if errors:
        print("\n⚠️ Found issues with the following primers (they will be skipped):")
        for name, err in errors.items():
            print(f" - {name}: {err}")
            
    if not valid_primers:
        print("\nNo valid primers to analyze. Aborting.")
        sys.exit(1)

    print(f"\nSuccessfully loaded {len(valid_primers)} primers. Starting analysis...\n")

    results = {}
    for name, seq in valid_primers.items():
        results[name] = {"seq": seq, "status": "Waiting for P2 and P3 code"}
    
    print(results)
    
    print(f"\nDone! The report will be saved to: {args.output}")

if __name__ == "__main__":
    main()