# Segment Intersection Benchmarker

A Python-based toolset for generating, displaying, minimizing, and testing computational test cases. Designed for developers working on implementations that require precision evaluation and correctness testing.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
  - [displayer.py](#displayerpy)
  - [generator.py](#generatorpy)
  - [minimizer.py](#minimizerpy)
  - [tester.py](#testerpy)

---

## Features

- **Visual display** of test cases and intersection results
- **Random test case generation**
- **Minimization** of failing test cases for easier debugging
- **Automated testing** of implementations with accuracy checks

---

## Usage

### `displayer.py`

Visualizes a test case or returns the number of intersections (using Python's `Decimal` precision of 100).

```bash
python displayer.py -f path/to/testcase.txt -d
```

Without `-d`, it simply returns the number of intersections:

```bash
python displayer.py -f path/to/testcase.txt
```

---

### `generator.py`

Generates new test cases.

```bash
python generator.py
```

You can customize the script to control the number and complexity of generated cases.

---

### `minimizer.py`

Minimizes a failing test case that causes an error in a specific implementation.

```bash
python minimizer.py -t "python your_implementation.py" -i path/to/input.txt -o path/to/minimized_output.txt
```

**Arguments:**
- `-t`: Command to test the implementation
- `-i`: Input test case file
- `-o`: Output file for the minimized instance

---

### `tester.py`

Tests one or more implementations against a set of test cases and expected output files.

```bash
python tester.py -f test_cases/ -a accuracy_outputs/ -c "python impl1.py" "python impl2.py"
```

**Arguments:**
- `-f`: Path to a file or folder of test cases
- `-a`: Path to accuracy/reference output files
- `-c`: One or more implementation commands to test
