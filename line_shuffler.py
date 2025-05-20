import csv
import random


def shuffle_segments(input_path: str, output_path: str):
    with open(input_path, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        rows = list(reader)  # Load all rows into memory

    random.shuffle(rows)  # In-place shuffle

    with open(output_path, 'w', newline='') as outfile:
        fieldnames = ['x1', 'y1', 'x2', 'y2']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    shuffle_segments("streets.csv", "streets_shuffled.csv")
