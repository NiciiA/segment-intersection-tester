from functools import partial

from utils import *

main(lambda x: bin2float(x), partial(calculate_intersections_pairwise, epsilon=1e-9))
