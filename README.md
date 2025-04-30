# segment-intersection-tester

# Usage

Call any of the binaries with `-f FILENAME` to specify a csv input file, otherwise the default segment set of
`((1, 0), (0, 1)),
((0, 0.75), (1, 0.25)),
((0, 0.25), (1, 0.75)),
((0, 0), (1, 1))`
will be used.
Pass `-a` to also print all intersections (might increase running time).

# Output Format

The last three lines will contain
the found number of intersections, where each overlapping segment is counted as two intersection (at its beginning and
its end),
the time taken for computing the intersections in milliseconds,
and the memory used for the computation in terms of difference in RSS before and after the computation.

# Implementations

| Language | Library                   | Method             | Number Type                                   | Unique |
|----------|---------------------------|--------------------|-----------------------------------------------|--------|
| C++      | boost                     | pairwise           | {double, boost::multiprecision::mpq_rational} |        |
| C++      | leda                      | MULMULEY           | {double, leda rational}                       | U      |
| C++      | leda                      | SWEEP (BO)         | {double, leda rational}                       | U      |
| C++      | leda                      | BALABAN            | {double, leda rational}                       | U      |
| C++      | leda                      | TRIVIAL (pairwise) | {double, leda rational}                       | U      |
| C++      | CGAL                      | intersector        | EPECK                                         | U      |
| C++      | CGAL                      | arrangement        | EPECK                                         | U      |
| C++      | CGAL                      | pairwise           | EPECK                                         | U      |
| C++      | OGDF                      | BO                 | double                                        | U      |
| C++      | geos                      | geos               | double                                        |        |
| Python   | manual                    | pairwise           | {Decimal 5 - 100, double, Fraction}           |        |
| Python   | SweepIntersectorLib       | BO                 | double                                        | U      |
| Rust     | geo::sweep::Intersections | BO                 | double                                        |        |

EPECK = Exact_predicates_exact_constructions_kernel

# Test Sets

- ours
- LEDA
- from Open Street Map
- from Graph Drawings
- from Test Suites?

# ToDo

- unique intersection points?
- CGAL inexact (double) kernel 
- Rust Geo Examples / Test Cases:
  > Due to the limited precision of most float data-types, the calculated intersection point may be snapped to one of
  the end-points even though all the end-points of the two lines are distinct points. In such cases, this field is still
  set to `true`. Please refer test_case: `test_central_endpoint_heuristic_failure_1` for such an example.
- Real-world test data from Open Street Map (randomize segment length by 90%-110% to get proper intersections)
- Java JTS?
- find critical python Decimal precision
- leda/test/geo/d2_geo/segint_test.cpp CURVE_SWEEP?
- fix test_GEO
- LEDA: no overlapping segments with double?
