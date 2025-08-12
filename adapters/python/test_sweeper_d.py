import warnings
from itertools import starmap

from SweepIntersectorLib.SweepIntersector import SweepIntersector

from segintbench.run import *

warnings.filterwarnings("ignore", category=FutureWarning)


def postprocess(intersections):
    return list(*starmap(Point, inters[1:-1]) for inters in intersections.values())


isector = SweepIntersector()
main(bin2float, isector.findIntersections, postprocess)
