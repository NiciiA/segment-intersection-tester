# Segment Intersection Test Set

These tests are based on a simple CSV format where each line represents a segment:
```
x1;y1;x2;y2
```

Floating-point numbers can behave differently across languages when converted from strings. For consistency, we store coordinates as raw IEEE 754 64-bit binary values in CSV files.

This avoids rounding issues and parsing differences, especially near precision limits.  
For example:
- Python accepts `5e-324` as valid.
- C++ throws an error for the same string.

By storing binary directly, we ensure consistent results in all tested environments.

---

Test case files are named to include key metadata:

```
{name}_{a}_{b}.csv
```

Where:  
- `name` = test case label  
- `a` = version index  
- `b` = number of segments (optional)

**Example:**  
`multi_axis_4.csv` indicates the 4th version of the `multi_axis` test case.

---

The test data is also:
- **Randomized** in segment length using `/utils/length_randomizer.py`
- **Shuffled** in order using `/utils/line_shuffler.py`

---

## Table of Contents
1. [Parallel and Collinear](#1-parallel-and-collinear)
2. [Length 0](#2-length-0)
3. [Multi-Axis](#3-multi-axis)
4. [Star Intersections](#4-star-intersections)
    - [Performance Test 1 (Star Intersections 9)](#41-performance-test-1-test-9)
    - [Performance Test 2 (Star Intersections 10)](#42-performance-test-2-test-10)
    - [Integer Test (Star Intersections 11)](#43-integer-test-test-11)
5. [Accuracy](#5-accuracy)
6. [Random](#6-random)
7. [Clustered](#7-clustered)
8. [Rounding](#8-rounding)

---

In computational geometry, a set of constraints on the input set of segments \( S \) is often assumed, which can simplify the implementation. Typical constraints include no segments being collinear, no three segments intersecting at the same point, no two events (such as segment endpoints or intersection points) occurring at the same \( x \)-value, and segments having positive length. However, these assumptions may not align with real-world data, making it critical to test for these positions to validate that the algorithm behaves correctly under non-ideal conditions.

---

## 1. Parallel and Collinear
![1.1 Parallel and Collinear](imgs/collinear_separate.svg)
![1.2 Parallel and Collinear](imgs/parallel_separate.svg)

When implementations use the matrix-based method, the determinant of the matrix is equal to zero when two segments are parallel or collinear.

**Expected behavior**: To correctly process collinear segments, an additional check is required if the determinant is zero. The approach used in our testing is the following:

To check for overlapping points of two collinear segments,  
\( s_1 = (p₁, p₂) \) and \( s_2 = (q₁, q₂) \),  
where points are given as \( pᵢ = (xᵢ, yᵢ) \) and \( qᵢ = (x'ᵢ, y'ᵢ) \),  
we perform the following steps:

1. Order the endpoints of each segment such that  
   \( p₁.x ≤ p₂.x \) and \( q₁.x ≤ q₂.x \).

2. If \( p₂.x < q₁.x \) or \( q₂.x < p₁.x \),  
   then there is no overlap, and we return an empty set of intersections.

3. Otherwise, define the overlapping segment as:  
   \( \text{overlap\_start} = \max(p₁, q₁) \)  
   \( \text{overlap\_end} = \min(p₂, q₂) \)  
   where max and min are taken with respect to the x-coordinate,  
   and if equal, the y-coordinate.

The resulting interval  
\[ \text{[overlap\_start, overlap\_end]} \]  
represents the points of intersection between the two collinear segments.

**Possible Error**:  
When the determinant is zero, failing to distinguish between parallel and collinear segments results in missing intersections.

---

## 2. Length 0
![2. Length 0](imgs/length_0.svg)

Length-0 segments can be considered single points, as their start and endpoint coincide, resulting in a non-positive length. In this context, we allow length-0 segments. When using the matrix-based approach, the following determinant becomes zero:

```
| x_b - x_a   x_d - x_c |   | 0  0 |
| y_b - y_a   y_d - y_c | = | 0  0 | = 0
```

This produces a special case similar to collinear segments and must be handled separately.

**Expected Behavior**:  
To correctly process intersections of two length-0 segments, an additional check is required after determining that the determinant is zero. The approach used in our testing is:

If  
- a_x == c_x and  
- a_y == c_y and  
- b_x == d_x and  
- b_y == d_y  
then the segments intersect.

**Possible Error**:  
When the determinant is zero, failing to handle length-0 intersections correctly can lead to missed intersections.

---

## 3. Multi-Axis
![3. Multi-Axis](imgs/multi_axis.svg)

As events (either segment endpoints or intersections) occur, they are sorted in a queue by priority, determined by the x-coordinate of each event. A simple priority queue implementation might use an array of tuples, where each tuple consists of a priority value (the x-coordinate) and the event itself. Handling multiple events with the same priority can vary across libraries; some implementations restrict the input set to prevent multiple events from occurring at the same x-coordinate.

**Expected Behavior**:  
Duplicate priorities should be managed to ensure correct processing order, with the sequence of events in the queue being: start point, intersection, then endpoint.

**Possible Error**:  
May result in missing intersections due to improper handling of duplicate priorities.

**Performance**:  
This scenario can also be useful for testing performance because having many points of interest on the same axis can create a computational bottleneck. When multiple events occur at the same x-coordinate, the algorithm must handle the ordering in the priority queue efficiently. Using an inefficient data structure in this context can lead to degraded performance.

---

## 4. Star Intersections
![4. Star Intersections](imgs/star_intersections.svg)

To illustrate potential issues, consider the Bentley-Ottmann algorithm with an input set \( S \) of three segments:  
\( S = { s₁, s₂, s₃ } \).  
The two segments \( s₁ \) and \( s₂ \) are supposed to intersect very close to one another before each of them intersects with segment \( s₃ \), forming a kind of star-shaped intersection.

**Expected Behavior**:  
\( s₁ \) and \( s₂ \) intersect just before the sweep line reaches the intersection point of \( s₁ \) and \( s₃ \), allowing the binary search tree (BST) to correctly reorder the segments.  
The algorithm then correctly detects that \( s₂ \) also intersects with \( s₃ \), since \( s₂ \) is correctly placed next to \( s₃ \) in the tree.

**Potential Error Due to Floating-Point Imprecision**:  
If the intersection point of \( s₁ \) and \( s₂ \) is at \( pₓ = 2.9999998875 \), but gets rounded to \( pₓ = 3 \), it can be incorrectly placed after the intersection of \( s₁ \) and \( s₃ \) (also at \( pₓ = 3 \)).  
As a result, the algorithm fails to reorder the segments at the correct moment. Since it only checks neighboring segments for intersections, it misses the one between \( s₂ \) and \( s₃ \), resulting in an incomplete solution.

---

## 4.1 Performance Test 1 (Test 9)
![4.1 Performance Test 1 (Test 9)](imgs/perf_test_1_tilted_top_safe.svg)

This test evaluates performance for segment sets where the number of intersections is relatively low.  
It uses the `star_intersection_9` (si9) dataset, which averages **0.75 intersections per segment**.  
For example, with 1000 segments, there are approximately 750 intersections.

The goal is to highlight performance differences between naive \( O(n^2) \) pairwise comparison algorithms (e.g. BOOST) and more efficient sweep-line approaches with \( O((n + k) \cdot \log n) \) complexity.

---

## 4.2 Performance Test 2 (Test 10)
![4.2 Performance Test 2 (Test 10)](imgs/perf_test_1_tilted_top_safe.svg)

This test increases intersection density using the `star_intersection_10` (si10) dataset, which has  
**5 intersections per segment**. With 1000 segments, that results in around 5000 intersections.

The higher density stresses the handling of \( k \), the number of intersections, and further contrasts performance between naive and optimized algorithms.

---

## 4.3 Integer Test (Test 11)
![4.3 Integer Test (Test 11)](imgs/star_intersections.svg)

Segments with strictly integer coordinates:
- Checks for precision and correctness in integer-only space

---

## 5. Accuracy
![5. Accuracy](imgs/accuracy.svg)

The widely used IEEE 754 double-precision standard imposes a significant constraint due to limited memory space for storing floating-point values. In the case of doubles, this allocation is 64 bits. The maximum finite value is approximately 1.7976931348623157 × 10³⁰⁸.

Now, consider two numbers, `a` and `b`, that are both close to this maximum value. When these numbers are multiplied, the resulting product can exceed the 64-bit capacity, potentially causing a memory overflow. Therefore, libraries will be tested for their accuracy in such computations.

To evaluate accuracy, the Euclidean distance will be used. The true values of intersection points are calculated using both floating-point doubles and exact rational numbers to support multiple numeric representations. Accuracy is assessed on distinct `x` and `y` coordinate pairs, since some libraries only return unique intersection points.

The Euclidean distance between the `true` and `approximation` point is defined as:

```
distance = sqrt((x_true - x_approx)² + (y_true - y_approx)²)
```

---

## 6. Random
![6.1 Random](imgs/random_1.svg)
![6.2 Random](imgs/random_2.svg)

This tests a large number of random segments with varying orientations and lengths to evaluate robustness under unpredictable input.  
Useful for uncovering edge cases and unexpected behavior in intersection logic.

---

## 7. Clustered
![7. Clustered](imgs/clustered_1.svg)

This tests segments densely packed in a small region to simulate high-intersection zones.  
It is useful for evaluating performance and correctness under geometric congestion.

---

## 8. Rounding
![8. Rounding](imgs/rounding.svg)

Cases that are sensitive to rounding:
- Intersections near coordinate boundaries
- **Includes the same tests as above but rotated vertically**