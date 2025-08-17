#!/bin/env python

from decimal import Decimal, getcontext

from segintbench.run import *

getcontext().prec = 5

main(lambda x: Decimal(bin2float(x)), calculate_intersections_pairwise)
