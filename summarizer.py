import csv
import argparse
from collections import defaultdict
from tabulate import tabulate

def summarize_results(csv_path, commands, output_md):
    # commands: list of substrings to filter by (case-sensitive)
    summary = defaultdict(dict)
    inputs_set = set()

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_command = row.get("command", "").strip()
            input_file = row.get("input", "").strip()
            result = row.get("result", "").strip()

            # Check if any of the short commands are substrings of full_command
            if not any(short_cmd in full_command for short_cmd in commands):
                continue

            summary[input_file][full_command] = result
            inputs_set.add(input_file)

    sorted_inputs = sorted(inputs_set)
    # For columns, show the matching full commands sorted
    # Collect all unique full commands from summary for header
    full_commands = set()
    for v in summary.values():
        full_commands.update(v.keys())
    sorted_full_commands = sorted(full_commands)

    table = []
    for inp in sorted_inputs:
        row = [inp]
        for cmd in sorted_full_commands:
            cell = summary[inp].get(cmd, "")
            row.append(cell)
        table.append(row)

    headers = ["Input"] + sorted_full_commands

    md_table = tabulate(table, headers=headers, tablefmt="github")

    with open(output_md, "w") as f:
        f.write(md_table)

    print(f"Markdown table saved to {output_md}")


def main():
    parser = argparse.ArgumentParser(description="Summarize results CSV by input and command.")
    parser.add_argument("-c", "--commands", required=True,
                        help="Comma-separated list of commands to include")
    parser.add_argument("-f", "--file", default="results.csv",
                        help="CSV file to read (default: results.csv)")
    parser.add_argument("-o", "--output", default="summary.md",
                        help="Output Markdown file (default: summary.md)")

    args = parser.parse_args()
    commands = [c.strip() for c in args.commands.split(",")]

    summarize_results(args.file, commands, args.output)

if __name__ == "__main__":
    main()
