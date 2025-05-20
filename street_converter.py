import csv
import json
import struct


def float_to_bin(number: float, as_hex: bool = False, single_precision: bool = False) -> str:
    """Convert a float to its binary or hex representation (big-endian)."""
    format_char = '>f' if single_precision else '>d'
    packed = struct.pack(format_char, number)
    base, width = (hex, 2) if as_hex else (bin, 8)
    return ''.join(base(b)[2:].rjust(width, '0') for b in packed)


def extract_segments_from_geojson(filepath: str):
    """Yield segments as (x1, y1, x2, y2) from a GeoJSON file."""
    with open(filepath, 'r') as f:
        geojson = json.load(f)

    for feature in geojson.get("features", []):
        coords = feature.get("geometry", {}).get("coordinates", [])
        for i in range(len(coords) - 1):
            yield coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1]


def write_segments_to_csv(segments, output_path: str, binary_encode=False):
    """Write segments to a CSV with optional binary-encoded float values."""
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['x1', 'y1', 'x2', 'y2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for x1, y1, x2, y2 in segments:
            if binary_encode:
                row = {
                    'x1': float_to_bin(x1),
                    'y1': float_to_bin(y1),
                    'x2': float_to_bin(x2),
                    'y2': float_to_bin(y2)
                }
            else:
                row = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

            writer.writerow(row)


if __name__ == "__main__":
    input_geojson = "streets.geojson"
    output_csv = "streets.csv"
    segments = extract_segments_from_geojson(input_geojson)
    write_segments_to_csv(segments, output_csv, binary_encode=True)
