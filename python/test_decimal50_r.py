from decimal import Decimal, getcontext

from utils import *

getcontext().prec = 50

main(lambda x: Decimal(bin2float(x)), calculate_intersections_pairwise)
