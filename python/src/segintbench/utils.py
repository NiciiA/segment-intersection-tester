import itertools
import math
import os
import re
from collections import namedtuple
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple

import click

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

    def slope(self):
        return slope(self.p1, self.p2)


# Function to get memory usage
def get_memory_usage():
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Memory usage in bytes


def slope(a, b):
    dx = Fraction(a.x) - b.x
    dy = Fraction(a.y) - b.y
    if dx == 0:
        return None
    else:
        if dx < 0:
            dx, dy = -dx, -dy
        return dy / dx


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

    det = (dx1 * dy2) - (dx2 * dy1)
    det1 = (dx1 * dy3) - (dx3 * dy1)
    det2 = (dx2 * dy3) - (dx3 * dy2)

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
        if ((det > 0 and 0.0 <= det1 <= det and 0.0 <= det2 <= det) or
                (det < 0 and 0.0 >= det1 >= det and 0.0 >= det2 >= det)):
            t = det2 / det
            yield Point(x1 + t * dx1, y1 + t * dy1)


# Function to find collinear intersections
def find_collinear_intersections(seg1, seg2, conv=lambda x: x):
    points1 = sorted([seg1.p1, seg1.p2])
    points2 = sorted([seg2.p1, seg2.p2])

    if points1[1].x < points2[0].x or points2[1].x < points1[0].x:
        return

    overlap_start = max(points1[0], points2[0])
    overlap_end = min(points1[1], points2[1])

    if overlap_start == overlap_end:
        yield conv(overlap_start)
    else:
        yield conv(overlap_start)
        yield conv(overlap_end)


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


def write_segments_to_csv(segments, file: str, binary_encode=True):
    """Write segments to a CSV with optional binary-encoded float values."""
    import csv
    if isinstance(file, (str, Path)):
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        file = open(file, 'w', newline='')
    with file as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(['x1', 'y1', 'x2', 'y2'])

        for seg in segments:
            if binary_encode:
                writer.writerow(map(float2bin, seg.coords()))
            else:
                writer.writerow(seg.coords())


def read_segments_from_csv(file: str, decode=bin2float):
    if isinstance(file, (str, Path)):
        file = open(file, 'r')
    with file as csvfile:
        header = next(csvfile).strip()
        if header != "x1;y1;x2;y2":  # Skip the header line
            raise IOError(f"Invalid CSV header {header!r}.")
        for line in csvfile:
            yield Segment.build(map(decode, line.strip().split(';')))


def parse_timeout(val):
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            from datetime import time
            t = time.fromisoformat(val)
            return ((t.hour * 60) + t.minute) * 60 + t.second
    else:
        return val


def get_command_file(cmdline):
    return Path(cmdline.split(" ")[-1])  # simple heuristic that works for all commands above


def parse_files(files, default_ext, exclude=None):
    for file in files:
        path = Path(file)
        if path.is_file() and (not exclude or not re.search(exclude, str(file))):
            yield path
            continue
        elif path.is_dir():
            iter = path.rglob(default_ext)
        elif re.search(r"[*?\[]", file):
            iter = Path('.').glob(file)
        else:
            raise click.UsageError(f"Invalid file/directory: {file}")
        if exclude:
            for file in iter:
                if not re.search(exclude, str(file)):
                    yield file
        else:
            yield from iter
