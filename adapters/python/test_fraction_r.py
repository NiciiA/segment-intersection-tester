from fractions import Fraction

from segintbench.run import *

main(lambda x: Fraction(bin2float(x)), calculate_intersections_pairwise)
