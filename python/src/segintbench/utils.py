import itertools
import math
import os
from collections import namedtuple
from pathlib import Path
from typing import NamedTuple

Point = namedtuple('Point', 'x y')


class Segment(NamedTuple):
    p1: Point
    p2: Point

    @classmethod
    def build(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            return cls.build(*args[0])
        elif len(args) == 4 and len(kwargs) == 0:
            return cls(Point(args[0], args[1]), Point(args[2], args[3]))
        elif len(args) + len(kwargs) <= 2:
            return cls(*args, **kwargs)
        else:
            return cls(*cls.points_from_coords(*args, **kwargs))

    @classmethod
    def points_from_coords(cls, x1, y1, x2, y2, *coords):
        yield Point(x1, y1)
        yield Point(x2, y2)
        if len(coords) == 0:
            return
        if (len(coords) % 2) != 0:
            raise ValueError("The number of coordinates must be even.")
        for x, y in itertools.pairwise(coords):
            yield Point(x, y)

    def coords(self):
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y

    def map(self, fn):
        return self.build(map(fn, self.coords()))

    def scale(self, factor):
        """Extend or shrink a segment from (x1,y1) to (x2,y2) by the given factor."""
        x1, y1, x2, y2 = self.coords()
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)

        if length == 0:
            return self.build(x1, y1, x2, y2)  # Can't scale a zero-length segment

        scale = factor
        new_dx = dx * scale
        new_dy = dy * scale
        return self.build(x1, y1, x1 + new_dx, y1 + new_dy)


# Function to get memory usage
def get_memory_usage():
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Memory usage in bytes


# Function to calculate the intersection of two segments
def find_intersection(seg1, seg2, epsilon=None, conv=lambda x: x):
    x1, y1 = conv(seg1.p1.x), conv(seg1.p1.y)
    x2, y2 = conv(seg1.p2.x), conv(seg1.p2.y)
    x3, y3 = conv(seg2.p1.x), conv(seg2.p1.y)
    x4, y4 = conv(seg2.p2.x), conv(seg2.p2.y)

    dx1 = x2 - x1
    dx2 = x4 - x3
    dy1 = y2 - y1
    dy2 = y4 - y3
    dx3 = x1 - x3
    dy3 = y1 - y3

    det = dx1 * dy2 - dx2 * dy1
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det == 0:
        if det1 != 0.0 or det2 != 0.0:
            return

        yield from find_collinear_intersections(seg1, seg2)
        return

    s = det1 / det
    t = det2 / det

    if epsilon:
        if 0.0 - epsilon <= s <= 1.0 + epsilon and 0.0 - epsilon <= t <= 1.0 + epsilon:
            yield Point(x1 + t * dx1, y1 + t * dy1)
    else:
        if 0.0 <= s <= 1.0 and 0.0 <= t <= 1.0:
            yield Point(x1 + t * dx1, y1 + t * dy1)


# Function to find collinear intersections
def find_collinear_intersections(seg1, seg2, conv=lambda x: x):
    pconv = lambda p: Point(conv(p.x), conv(p.y))
    points1 = sorted(map(pconv, [seg1.p1, seg1.p2]), key=lambda p: (p.x, p.y))
    points2 = sorted(map(pconv, [seg2.p1, seg2.p2]), key=lambda p: (p.x, p.y))

    if points1[1].x < points2[0].x or points2[1].x < points1[0].x:
        return

    overlap_start = max(points1[0], points2[0], key=lambda p: (p.x, p.y))
    overlap_end = min(points1[1], points2[1], key=lambda p: (p.x, p.y))

    if overlap_start == overlap_end:
        yield overlap_start
    else:
        yield overlap_start
        yield overlap_end


# Function to calculate intersections for all segment pairs
def calculate_intersections_pairwise(segments, epsilon=None, conv=lambda x: x):
    for seg1, seg2 in itertools.combinations(segments, 2):
        yield from find_intersection(seg1, seg2, epsilon, conv)


def bin2float(binary_string, single_precision: bool = False):
    import struct
    if len(binary_string) != (32 if single_precision else 64):
        raise ValueError("Binary string length must be 32 (for float) or 64 (for double).")
    byte_data = int(binary_string, 2).to_bytes(4 if single_precision else 8, byteorder='big')
    return struct.unpack('>f' if single_precision else '>d', byte_data)[0]


def float2bin(number: float, as_hex: bool = False, single_precision: bool = False) -> str:
    """Convert a float to its binary or hex representation (big-endian)."""
    import struct
    format_char = '>f' if single_precision else '>d'
    packed = struct.pack(format_char, number)
    base, width = (hex, 2) if as_hex else (bin, 8)
    return ''.join(base(b)[2:].rjust(width, '0') for b in packed)


def write_segments_to_csv(segments, output_path: str, binary_encode=True):
    """Write segments to a CSV with optional binary-encoded float values."""
    import csv
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(['x1', 'y1', 'x2', 'y2'])

        for seg in segments:
            if binary_encode:
                writer.writerow(map(float2bin, seg.coords()))
            else:
                writer.writerow(seg.coords())


def read_segments_from_csv(file: str, decode=bin2float):
    with open(file, 'r') as file:
        header = next(file).strip()
        if header != "x1;y1;x2;y2":  # Skip the header line
            raise IOError(f"Invalid CSV header {header!r}.")
        for line in file:
            yield Segment.build(map(decode, line.strip().split(';')))
