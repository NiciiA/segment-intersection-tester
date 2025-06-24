import pandas as pd
from pathlib import Path
from tabulate import tabulate

def find_csv_files(directory):
    return list(Path(directory).rglob("*.csv"))

def load_and_process_csvs(files):
    results, times, memories, distances = [], [], [], []

    for file in files:
        try:
            df = pd.read_csv(file)
            file_info = {"file": file.relative_to(Path.cwd())}

            # Assume single-row CSVs with expected columns
            row = df.iloc[0].to_dict()
            for key in ["result", "time", "memory", "distance"]:
                value = row.get(key)

                if key == "result" and value is not None:
                    results.append({**file_info, "result": value})
                if key == "time" and value is not None:
                    times.append({**file_info, "time": value})
                if key == "memory" and value is not None:
                    memories.append({**file_info, "memory": value})
                if key == "distance" and value is not None:
                    distances.append({**file_info, "distance": value})

        except Exception as e:
            print(f"Error reading {file}: {e}")

    return results, times, memories, distances

def write_markdown_tables(results, times, memories, distances):
    tables = {
        "merged_results.md": (results, "result"),
        "merged_time.md": (times, "time"),
        "merged_memory.md": (memories, "memory"),
        "merged_distance.md": (distances, "distance"),
    }

    for filename, (data, _) in tables.items():
        if not data:
            continue
        with open(filename, "w") as f:
            f.write(tabulate(data, headers="keys", tablefmt="pipe"))
            f.write("\n")
        print(f"Wrote {filename}")

def main(directory="."):
    csv_files = find_csv_files(directory)
    results, times, memories, distances = load_and_process_csvs(csv_files)
    write_markdown_tables(results, times, memories, distances)

if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    main(target_dir)
