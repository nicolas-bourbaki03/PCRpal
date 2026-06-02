# report.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os
import random


def save_csv(results, output_path):
    """
    Saves analysis results to a CSV file.
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

    print(f"  CSV report saved to: {output_path}")


def plot_gc_tm_multi(all_results, output_path="output/gc_vs_tm.png", max_points=500):
    """
    Scatter plot: Tm vs GC content, one color per input file.
    Samples up to max_points per dataset for readability.
    """
    colors = ['steelblue', 'tomato', 'seagreen', 'darkorange', 'mediumpurple']

    plt.figure(figsize=(12, 7))

    for i, (label, results) in enumerate(all_results.items()):
        # sample if too many points
        sample = random.sample(results, min(max_points, len(results)))
        gc = [r['gc_content'] for r in sample]
        tm = [r['tm_wallace'] for r in sample]
        color = colors[i % len(colors)]
        plt.scatter(gc, tm, color=color, edgecolors='none',
                    alpha=0.5, s=20, label=f"{label} (n={len(results)})")

    plt.axvline(x=40, color='red', linestyle='--', linewidth=1, label='GC min (40%)')
    plt.axvline(x=60, color='red', linestyle='--', linewidth=1, label='GC max (60%)')

    plt.xlabel('GC Content (%)')
    plt.ylabel('Melting Temperature Tm (°C)')
    plt.title('Tm vs GC Content per Dataset')
    plt.legend(loc='upper left')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Scatter plot saved to: {output_path}")


def plot_flags_multi(all_results, output_path="output/flags_summary.png"):
    """
    Bar chart: percentage of flagged primers per dataset, grouped by flag type.
    all_results: dict {label: [list of result dicts]}
    """
    labels = list(all_results.keys())
    flag_types = ['gc_out', 'length_out', 'self_comp', 'dimer']
    flag_labels = ['GC out of range', 'Length out of range',
                   'Self-complementarity', 'Primer dimer']
    colors = ['tomato', 'darkorange', 'steelblue', 'seagreen']

    x = range(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 2), 6))

    for i, (flag, flag_label, color) in enumerate(zip(flag_types, flag_labels, colors)):
        percentages = []
        for label in labels:
            results = all_results[label]
            total = len(results)
            if total == 0:
                percentages.append(0)
                continue
            if flag == 'gc_out':
                count = sum(1 for r in results if not r['gc_ok'])
            elif flag == 'length_out':
                count = sum(1 for r in results if not r['length_ok'])
            elif flag == 'self_comp':
                count = sum(1 for r in results if r['self_complementarity'])
            elif flag == 'dimer':
                count = sum(1 for r in results if r['dimer'])
            percentages.append(round(count / total * 100, 1))

        offset = [xi + i * width for xi in x]
        bars = ax.bar(offset, percentages, width, label=flag_label, color=color, alpha=0.8)

        # add % labels on bars
        for bar, pct in zip(bars, percentages):
            if pct > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.5,
                        f'{pct}%', ha='center', va='bottom', fontsize=8)

    ax.set_xticks([xi + width * 1.5 for xi in x])
    ax.set_xticklabels(labels, rotation=15, ha='right')
    ax.set_ylabel('Flagged primers (%)')
    ax.set_title('Primer Quality Flags by Dataset')
    ax.legend(loc='upper right')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Flag summary chart saved to: {output_path}")