from enum import Enum, auto

import numpy as np
import pandas as pd


class IntersectionType(Enum):
    TRUE_INTERSECTION = auto()
    POINT_OVERLAP = auto()
    SEGMENT_OVERLAP = auto()


def find_collinear_intersections_vect(seg1p1, seg1p2, seg2p1, seg2p2):
    if seg1p1 > seg1p2:
        seg1p1, seg1p2 = seg1p2, seg1p1
    if seg2p1 > seg2p2:
        seg2p1, seg2p2 = seg2p2, seg2p1

    if seg1p2[0] < seg2p1[0] or seg2p2[0] < seg1p1[0]:
        return

    overlap_start = max(seg1p1, seg2p1)
    overlap_end = min(seg1p2, seg2p2)

    if overlap_start == overlap_end:
        yield IntersectionType.POINT_OVERLAP, (seg1p1, seg1p2), (seg2p1, seg2p2), overlap_start
    else:
        yield IntersectionType.SEGMENT_OVERLAP, (seg1p1, seg1p2), (seg2p1, seg2p2), overlap_start, overlap_end


def find_intersections_vect(df1, df2):
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    dx1 = df1['x2'] - df1['x1']
    dx2 = df2['x2'] - df2['x1']
    dy1 = df1['y2'] - df1['y1']
    dy2 = df2['y2'] - df2['y1']
    dx3 = df1['x1'] - df2['x1']
    dy3 = df1['y1'] - df2['y1']

    ddf = pd.DataFrame({
        'det': dx1 * dy2 - dx2 * dy1,
        'det1': dx1 * dy3 - dx3 * dy1,
        'det2': dx2 * dy3 - dx3 * dy2
    })

    sel = (0 <= ddf['det1']) & (ddf['det1'] <= ddf['det']) & (0 <= ddf['det2']) & (ddf['det2'] <= ddf['det'])
    for index, row in ddf[sel].iterrows():
        seg1 = (df1['x1'][index], df1['y1'][index]), (df1['x2'][index], df1['y2'][index])
        seg2 = (df2['x1'][index], df2['y1'][index]), (df2['x2'][index], df2['y2'][index])
        if row['det'] == 0:
            yield from find_collinear_intersections_vect(*seg1, *seg2)
        else:
            t = row['det2'] / row['det']
            p = df1['x1'][index] + t * dx1[index], df1['y1'][index] + t * dy1[index]
            yield IntersectionType.TRUE_INTERSECTION, seg1, seg2, p


def calculate_intersections_vectorized(segments):
    if isinstance(segments, pd.DataFrame):
        df = segments
    else:
        df = pd.DataFrame((s.coords() for s in segments), columns=["x1", "y1", "x2", "y2"])
    for i in range(1, len(df)):
        yield from find_intersections_vect(df.iloc[i:], df.iloc[:-i])
