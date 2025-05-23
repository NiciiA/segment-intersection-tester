import warnings

from SweepIntersectorLib.SweepIntersector import SweepIntersector

from utils import *

warnings.filterwarnings("ignore", category=FutureWarning)


def postprocess(intersections):
    unique_intersections = set()
    for seg, intersections in intersections.items():
        unique_intersections.update(intersections[1:-1])


isector = SweepIntersector()
main(bin2float, isector.findIntersections, postprocess)
