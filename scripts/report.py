# report

import matplotlib.pyplot as plt
import csv

def save_csv(results, output_path):
    """
    Saves analysis results to a CSV file.
    results: list of dicts {name, sequence, tm, gc, length, flags}
    output_path: str, path to output CSV file
    """
    pass

def plot_gc_tm(results, output_path):
    """
    Scatter plot: Tm vs GC content per primer.
    """
    pass

def plot_flags(results, output_path):
    """
    Bar chart: number of flagged issues per primer.
    """
    pass