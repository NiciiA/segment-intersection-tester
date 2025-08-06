import warnings
from itertools import starmap

from SweepIntersectorLib.SweepIntersector import SweepIntersector

from segintbench.run import *

warnings.filterwarnings("ignore", category=FutureWarning)


def postprocess(intersections):
    unique_intersections = set()
    for seg, intersections in intersections.items():
        # intersections includes start and end points of seg
        unique_intersections.update(starmap(Point,intersections[1:-1]))
    return unique_intersections


isector = SweepIntersector()
main(bin2float, isector.findIntersections, postprocess)
