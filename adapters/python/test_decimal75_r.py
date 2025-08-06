from decimal import Decimal, getcontext

from segintbench.run import *

getcontext().prec = 75

main(lambda x: Decimal(bin2float(x)), calculate_intersections_pairwise)
