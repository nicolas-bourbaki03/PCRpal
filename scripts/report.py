# report.py

import csv
import os
import matplotlib.pyplot as plt


def save_csv(results, output_path):
    """
    Saves analysis results to a CSV file.
    results: list of dicts with keys: name, sequence, tm, gc_content, length,
             gc_ok, length_ok, self_complementarity, dimer
    output_path: str, path to output CSV file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None

    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'name', 'sequence', 'length', 'tm_wallace',
            'gc_content', 'gc_ok', 'length_ok',
            'self_complementarity', 'dimer'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"CSV report saved to: {output_path}")


def plot_gc_tm(results, output_path="output/gc_vs_tm.png"):
    """
    Scatter plot: Tm vs GC content per primer.
    """
    names = [r['name'] for r in results]
    gc = [r['gc_content'] for r in results]
    tm = [r['tm_wallace'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.scatter(gc, tm, color='steelblue', edgecolors='black', alpha=0.7)

    for i, name in enumerate(names):
        plt.annotate(name[:15], (gc[i], tm[i]), fontsize=6, alpha=0.6)

    plt.axvline(x=40, color='red', linestyle='--', linewidth=0.8, label='GC min (40%)')
    plt.axvline(x=60, color='red', linestyle='--', linewidth=0.8, label='GC max (60%)')

    plt.xlabel('GC Content (%)')
    plt.ylabel('Melting Temperature Tm (°C)')
    plt.title('Tm vs GC Content per Primer')
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Scatter plot saved to: {output_path}")


def plot_flags(results, output_path="output/flags.png"):
    """
    Bar chart: flagged issues per primer.
    """
    names = [r['name'][:20] for r in results]
    flags = []

    for r in results:
        count = 0
        if not r.get('gc_ok', True):
            count += 1
        if not r.get('length_ok', True):
            count += 1
        if r.get('self_complementarity', False):
            count += 1
        if r.get('dimer', False):
            count += 1
        flags.append(count)

    colors = ['green' if f == 0 else 'orange' if f == 1 else 'red' for f in flags]

    plt.figure(figsize=(max(10, len(names) * 0.5), 6))
    plt.bar(names, flags, color=colors, edgecolor='black')
    plt.xticks(rotation=45, ha='right', fontsize=7)
    plt.ylabel('Number of Flags')
    plt.title('Flagged Issues per Primer')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Flag chart saved to: {output_path}")


# quick test - can be removed later
if __name__ == "__main__":
    test_results = [
        {
            'name': 'primer_forward',
            'sequence': 'CCTCTGCGGTGCCAAGCCTC',
            'length': 20,
            'tm_wallace': 64,
            'gc_content': 65.0,
            'gc_ok': False,
            'length_ok': True,
            'self_complementarity': False,
            'dimer': True
        },
        {
            'name': 'primer_reverse',
            'sequence': 'CGTGGTGGTCCCGGCCGCC',
            'length': 19,
            'tm_wallace': 70,
            'gc_content': 78.9,
            'gc_ok': False,
            'length_ok': True,
            'self_complementarity': True,
            'dimer': True
        },
        {
            'name': 'primer_ok',
            'sequence': 'ATGCGTACGTAGCTAGCTA',
            'length': 19,
            'tm_wallace': 56,
            'gc_content': 47.4,
            'gc_ok': True,
            'length_ok': True,
            'self_complementarity': False,
            'dimer': False
        }
    ]

    save_csv(test_results, "output/test_report.csv")
    plot_gc_tm(test_results, "output/gc_vs_tm.png")
    plot_flags(test_results, "output/flags.png")