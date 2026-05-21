import argparse
import sys
import csv
from parser import load_and_validate

def save_report(results, output_file):
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['Name', 'Sequence', 'Status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for name, data in results.items():
                writer.writerow({
                    'Name': name,
                    'Sequence': data['seq'],
                    'Status': data['status']
                })
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="PCRpal - Batch validation and analysis of PCR primers."
    )
    parser.add_argument(
        "input", 
        help="Path to the input file (.csv or .fasta)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to the report file (.csv)", 
        default="pcrpal_report.csv"
    )
    
    args = parser.parse_args()

    print(f"--- PCRpal Starter ---")
    print(f"Loading: {args.input}")
    
    try:
        valid_primers, errors = load_and_validate(args.input)
    except FileNotFoundError:
        print(f"Error: File {args.input} does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    if errors:
        print(f"\nSkipped {len(errors)} invalid sequences (check logs).")
            
    if not valid_primers:
        print("\nNo valid primers found. Aborting.")
        sys.exit(1)

    print(f"Processing {len(valid_primers)} primers")

    results = {}
    for name, seq in valid_primers.items():
        short_name = name[:30] + "..." if len(name) > 33 else name
        
        results[short_name] = {
            "seq": seq, 
            "status": "Validated - Waiting for analysis"
        }
    if save_report(results, args.output):
        print(f"\nSuccess! Analysis saved to: {args.output}")
    else:
        print("\nFailed to save the report.")

if __name__ == "__main__":
    main()