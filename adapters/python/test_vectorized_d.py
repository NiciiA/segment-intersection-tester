#!/bin/env python

from segintbench.fast_inter import calculate_intersections_vectorized, IntersectionType
from segintbench.run import *


def postprocess(inp):
    out = []
    for i in inp:
        if i[0] == IntersectionType.SEGMENT_OVERLAP:
            out.append((float2bin(i[3][0]), float2bin(i[3][1])))
            out.append((float2bin(i[4][0]), float2bin(i[4][1])))
        else:
            out.append((float2bin(i[3][0]), float2bin(i[3][1])))
    return out


main(bin2float, calculate_intersections_vectorized, postprocess)
