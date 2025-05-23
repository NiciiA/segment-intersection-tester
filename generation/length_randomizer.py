import csv
import struct
import random
import math


def bin_to_float(bin_str: str, single=False) -> float:
    """Convert binary string to float (IEEE 754)."""
    byte_length = 4 if single else 8
    int_val = int(bin_str, 2)
    return struct.unpack('>f' if single else '>d', int_val.to_bytes(byte_length, byteorder='big'))[0]


def float_to_bin(value: float, single=False) -> str:
    """Convert float to binary string."""
    packed = struct.pack('>f' if single else '>d', value)
    return ''.join(bin(b)[2:].rjust(8, '0') for b in packed)


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
            x1 = bin_to_float(row['x1'])
            y1 = bin_to_float(row['y1'])
            x2 = bin_to_float(row['x2'])
            y2 = bin_to_float(row['y2'])

            # Randomize segment length by ±10%
            factor = random.uniform(0.9, 1.1)
            x1, y1, x2, y2 = scale_segment(x1, y1, x2, y2, factor)

            # Re-encode
            writer.writerow({
                'x1': float_to_bin(x1),
                'y1': float_to_bin(y1),
                'x2': float_to_bin(x2),
                'y2': float_to_bin(y2)
            })


if __name__ == "__main__":
    process_segments("streets.csv", "streets_randomized.csv")
