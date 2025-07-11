import csv
import argparse
import os

import matplotlib.pyplot as plt
from collections import defaultdict
import re

def extract_segment_count(input_filename):
    # Extracts the number at the end before ".csv"
    match = re.search(r"_(\d+)(?:\.csv)?$", input_filename)
    return int(match.group(1)) if match else None

def plot_runtimes(csv_path, command_filters, input_prefixes):
    data = defaultdict(lambda: defaultdict(float))  # {command: {segment_count: runtime}}

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_command = row.get("command", "").strip()
            input_path = row.get("input", "").strip()
            time = row.get("time", "").strip()

            if not any(c in full_command for c in command_filters):
                continue
            if not any(prefix in input_path for prefix in input_prefixes):
                continue

            seg_count = extract_segment_count(input_path)
            if seg_count is None:
                continue

            try:
                runtime = float(time)
            except ValueError:
                continue

            data[full_command][seg_count] = runtime

    # Plot
    plt.figure(figsize=(10, 6))
    for command, results in data.items():
        x = sorted(results.keys())
        y = [results[k] for k in x]
        label = os.path.basename(command)  # This shows just 'test_leda-mm-d' instead of full path
        plt.plot(x, y, marker='o', label=label)

    plt.xlabel("Number of segments")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Number of Segments")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("runtime_comparison.png")
    plt.show()
    print("Saved plot as 'runtime_comparison.png'.")

def main():
    parser = argparse.ArgumentParser(description="Plot runtime trends from results.csv")
    parser.add_argument("-c", "--commands", required=True,
                        help="Comma-separated list of command substrings")
    parser.add_argument("-f", "--inputs", required=True,
                        help="Comma-separated list of input filename prefixes (e.g., star_intersections_9)")
    parser.add_argument("--file", default="results.csv", help="CSV file path (default: results.csv)")
    args = parser.parse_args()

    command_filters = [c.strip() for c in args.commands.split(",")]
    input_prefixes = [f.strip() for f in args.inputs.split(",")]

    plot_runtimes(args.file, command_filters, input_prefixes)

if __name__ == "__main__":
    main()
