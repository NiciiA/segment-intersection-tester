import csv
import struct
import random
import math

from segintbench.utils import *


def scale_segment(x1, y1, x2, y2, factor):
    """Extend or shrink a segment from (x1,y1) to (x2,y2) by the given factor."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)

    if length == 0:
        return x1, y1, x2, y2  # Can't scale a zero-length segment

    scale = factor
    new_dx = dx * scale
    new_dy = dy * scale
    return x1, y1, x1 + new_dx, y1 + new_dy


def process_segments(input_path: str, output_path: str):
    with open(input_path, 'r', newline='') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['x1', 'y1', 'x2', 'y2']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            # Decode binary to float
            x1 = bin2float(row['x1'])
            y1 = bin2float(row['y1'])
            x2 = bin2float(row['x2'])
            y2 = bin2float(row['y2'])

            # Randomize segment length by ±10%
            factor = random.uniform(0.9, 1.1)
            x1, y1, x2, y2 = scale_segment(x1, y1, x2, y2, factor)

            # Re-encode
            writer.writerow({
                'x1': float2bin(x1),
                'y1': float2bin(y1),
                'x2': float2bin(x2),
                'y2': float2bin(y2)
            })


if __name__ == "__main__":
    process_segments("streets.csv", "streets_randomized.csv")
