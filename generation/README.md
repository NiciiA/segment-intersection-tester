# Segment Intersection Benchmarker

A Python-based toolset for generating, transforming, displaying, minimizing, and testing geometric segment intersection test cases. Designed for researchers and developers evaluating precision, performance, and correctness in geometric algorithms such as Mulmuley's.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [displayer.py](#displayerpy)
  - [generator.py](#generatorpy)
  - [minimizer.py](#minimizerpy)
  - [tester.py](#testerpy)
  - [number_converter.py](#numberconverterpy)
  - [street_exporter.py](#streetexporterpy)
  - [street_converter.py](#streetconverterpy)
  - [json_converter.py](#jsonconverterpy)
  - [ogdf_converter.py](#ogdfconverterpy)
  - [length_randomizer.py](#lengthrandomizerpy)
  - [line_shuffler.py](#lineshufflerpy)
- [Output Format](#output-format)
- [Directory Structure](#directory-structure)

---

## Features

- 📈 **Visual display** of test cases and segment intersections
- 🧪 **Random test case generation** with reproducible CSV output
- 🪓 **Minimization** of failing test cases for debugging
- 🔍 **Automated accuracy testing** across multiple implementations
- 🔁 **Format conversion**: CSV ⇄ JSON, GeoJSON, OGDF
- ⚙️ **Preprocessing tools**: Segment length randomization, order shuffling

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourname/segment-intersection-benchmarker.git
cd segment-intersection-benchmarker
pip install -r requirements.txt
```

---

## Usage

### `displayer.py`

Displays a test case graphically or returns the number of segment intersections.

```bash
# Display mode
python displayer.py -f path/to/testcase.txt -d

# Intersection count only
python displayer.py -f path/to/testcase.txt
```

---

### `generator.py`

Generates new test cases in CSV format.

```bash
python generator.py
```

---

### `minimizer.py`

Minimizes a failing test case to the smallest version that still causes failure.

```bash
python minimizer.py -t "python your_implementation.py" -i input.csv -o minimized.csv
```

---

### `tester.py`

Tests one or more implementations against test cases and reference outputs.

```bash
python tester.py -f test_cases/ -a test_cases/accuracy_outputs/ -c "python implementation1.py" "python implementation2.py"
```

---

### `number_converter.py`

Converts float coordinate CSV files to binary-encoded format (IEEE 754).

```bash
python number_converter.py -f input.csv -o output.csv
```

---

### `street_exporter.py`

Downloads street network data from OpenStreetMap as GeoJSON.

```bash
python street_exporter.py -p "1010, Vienna, Austria" -n drive -o streets.geojson
```

---

### `street_converter.py`

Converts `.geojson` street files into binary-encoded `.csv` files.

```bash
python street_converter.py
```

Scans the current directory for `.geojson` files and generates `.csv` files with the same base name.

---

### `json_converter.py`

Converts segment CSV files to a structured JSON array.

```bash
python json_converter.py -i input.csv -o output.json
```

---

### `ogdf_converter.py`

Converts segment data into `.gml` format for OGDF-based visualization tools.

```bash
python ogdf_converter.py -i input.csv -o output.gml
```

---

### `length_randomizer.py`

Randomly adjusts the length of each segment by ±10% while keeping direction.

```bash
python length_randomizer.py -i input.csv -o randomized.csv
```

---

### `line_shuffler.py`

Shuffles the order of segments in a CSV file.

```bash
python line_shuffler.py -i input.csv -o shuffled.csv
```

---

## Output Format

Generated or processed CSVs contain:

```
x1;y1;x2;y2
00001010;00000011;00001100;00000101
...
```

Binary strings represent integer or float coordinates, depending on the conversion pipeline.

---

## Directory Structure

```text
segment-intersection-benchmarker/
├── displayer.py
├── generator.py
├── minimizer.py
├── tester.py
├── number_converter.py
├── street_exporter.py
├── street_converter.py
├── json_converter.py
├── ogdf_converter.py
├── length_randomizer.py
├── line_shuffler.py
├── tests/
├── examples/
└── README.md
```
