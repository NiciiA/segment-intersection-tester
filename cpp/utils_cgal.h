#pragma once

#include "utils.h"

#ifndef CGAL_KERNEL
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#define CGAL_KERNEL CGAL::Exact_predicates_exact_constructions_kernel
#endif

typedef CGAL_KERNEL K;

typedef K::Point_2 CGAL_Point;
typedef K::Segment_2 CGAL_Segment;

std::vector<CGAL_Segment> cgal_segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2) {
	cgal_segments.emplace_back(
			CGAL_Segment(CGAL_Point(bitstring_to_double(x1), bitstring_to_double(y1)),
					CGAL_Point(bitstring_to_double(x2), bitstring_to_double(y2))));
}
