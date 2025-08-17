#!/bin/env python

from segintbench.fast_inter import calculate_intersections_vectorized, IntersectionType
from segintbench.run import *


def postprocess(inp):
    out = []
    for i in inp:
        if i[0] == IntersectionType.SEGMENT_OVERLAP:
            out.append(i[3])
            out.append(i[4])
        else:
            out.append(i[3])
    return out


main(lambda x: Fraction(bin2float(x)), calculate_intersections_vectorized, postprocess)
