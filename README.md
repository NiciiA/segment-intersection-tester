# segment-intersection-tester

A complete testing framework for evaluating segment intersection algorithms.
Includes a ready-to-deploy Docker environment, a suite of test generators, and support for integrating with a variety of intersection implementations.

---

## What is inside

- **Test Set Generator**  
  Automated tools to generate test sets for intersection evaluation.

- **Test Utilities (in `/generation`)**  
  A collection of tools to modify, convert, randomize, and analyze test data:
  - `generator.py` – main test case generator
  - `street_exporter.py` & `street_converter.py` – OpenStreetMap-based real-world test set extraction
  - `random_generator.py`, `length_randomizer.py`, `line_shuffler.py`, `minimizer.py` – utilities to transform or stress-test datasets
  - `json_converter.py`, `number_converter.py`, `ogdf_converter.py` – format converters
  - `export_all.py`, `displayer.py` – output management and visualization
  - `tester_accuracy.py` – utility to run precision-sensitive evaluations

- **Adapters**  
  Interface layers for plugging in different algorithm implementations or frameworks. List of implementations given below [Implementations](#implementations)

- **tester.py**  
  Script to run and evaluate all test sets.

- **build.sh**  
  Build script to prepare the Docker environment and install all dependencies.

- **Dockerfile**  
  The Dockerfile for the Docker environment.

---

# Implementations

| Language | Library                   | Method               | Number Type                                   | Unique |
|----------|---------------------------|----------------------|-----------------------------------------------|--------|
| C++      | boost                     | pairwise             | {double, boost::multiprecision::mpq_rational} |        |
| C++      | leda                      | MULMULEY             | {double, leda rational}                       | U      |
| C++      | leda                      | SWEEP (BO)           | {double, leda rational}                       | U      |
| C++      | leda                      | BALABAN              | {double, leda rational}                       |        |
| C++      | leda                      | TRIVIAL              | {double, leda rational}                       |        |
| C++      | leda                      | CURVE_SWEEP_SEGMENTS | leda rational                                 | U      |
| C++      | leda                      | pairwise             | {double, leda rational}                       |        |
| C++      | CGAL                      | intersector          | {Simple_cartesian<double>, EPECK}             |        |
| C++      | CGAL                      | arrangement          | {Simple_cartesian<double>, EPECK}             | U      |
| C++      | CGAL                      | pairwise             | {Simple_cartesian<double>, EPECK}             |        |
| C++      | OGDF                      | BO                   | double                                        | U      |
| C++      | geos                      | SimpleNoder          | double                                        |        |
| C++      | geos                      | MCIndexNoder         | double                                        |        |
| Python   | manual                    | pairwise             | {Decimal 5 - 100, double, Fraction}           |        |
| Python   | SweepIntersectorLib       | BO                   | double                                        | U      |
| Rust     | geo::sweep::Intersections | BO                   | double                                        |        |
| Java     | JTS                       | MCIndexNoder         | double                                        |        |

EPECK = Exact_predicates_exact_constructions_kernel

# Test Sets

- ours
- LEDA
- from Open Street Map
- from Graph Drawings
- from Test Suites?
- from GD Contest

---

## How to Use It

```bash
#!/bin/bash

source .venv/bin/activate

pushd generation

  python ./generator.py # standard test generator
  python ./generate_locations.py # location test generator

  pushd leda
    ./gen_leda.sh
  popd

popd # /generation

# TODO msc, GD Contest
```
```python
def do_generation():
run_in_dir("generation/generator", ["python", "./generation/generator.py"])
run_in_dir("generation/locations", ["python", "./generation/generate_locations.py"])

def do_testing():
run_in_dir("testing/tests", ["python", "./tester.py", "run-tests", "./data/segment-intersection-data/tests/*"])
run_in_dir("testing/loctests", ["python", "./tester.py", "run-tests", "./data/segment-intersection-data/tests_location/*"])
run_in_dir("testing/collecter", ["python", "./tester.py", "collect", "./out", "results.csv"])
```

1. **Generate test sets**  
   Run the generator to create test inputs:
   ```bash
   python generation/generator.py
   ```

2. **Set up the Docker environment**  
   Build the container using the provided Dockerfile:
   ```bash
   docker build -t segment-tester .
   ```

3. **Run the tests inside Docker**  
   Start the container and execute the tester:
   ```bash
   docker run --rm -v $(pwd):/app segment-tester python tester.py
   ```

4. **Copy the results from Docker to your local environment**  
   If needed:
   ```bash
   docker cp <container_id>:/app/results ./results
   ```

5. **Inspect the results**  
   Review output logs, accuracy stats, and any exported result files under the `/results` directory.


---

# Notes

- unique intersection points? => `uniq`
- LEDA: no overlapping segments with double
- CGAL Curve Sweep [no]

# Meeting 08.05.

- (NF) Docker Container + Repro Script
    - Tests laufen lassen
- (NA) Open Street Map Test Data
    - Real-world test data from Open Street Map (randomize segment length by 90%-110% to get proper intersections)
    - (NF) send python script
- (NF) Grap Drawing Test Data (GD Contest) [done]
    - https://github.com/5gon12eder/msc-graphstudy/#graphs-graphscfg
    - https://sparse.tamu.edu/about
- (MS) LEDA Test Daten
    - star intersection vergleich
- (MS) LEDA Tester checken
- (NF) CGAL inexact (double) kernel [done]
- (NF) geos/JTS different indexers [done]
- (NA) Java JTS [done]
- (NF) fix test_GEO [done]
- (NA) Rust Geo Examples / Test Cases: [done]
  > Due to the limited precision of most float data-types, the calculated intersection point may be snapped to one of
  the end-points even though all the end-points of the two lines are distinct points. In such cases, this field is still
  set to `true`. Please refer test_case: `test_central_endpoint_heuristic_failure_1` for such an example.
- (NF) find critical python Decimal precision
- (MS) leda/test/geo/d2_geo/segint_test.cpp CURVE_SWEEP?
- (NA) shuffle input file
- (NA) rotate benchmark sets
- (NF) robust reading links an Manu
- (NA) integer test sets
- (NF) boost r-tree (GDA team 4)

# Questions

- ground truth: quadratic with rational - how many errors?
- double: how many more errors through BO over quadratic-double?

# ToDo

- rational inputs for adapters
- compress files?
- convert data sets
- Merge Data Sets (Nico, LEDA Test Data from Manu)
- Johannes:
  - Cluster Runner
  - Docker / Dependencies auf Cluster
  - SLURM?
  - Shared Folder






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
