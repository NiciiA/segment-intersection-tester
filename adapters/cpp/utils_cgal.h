#pragma once

#include "utils.h"

#include <CGAL/Simple_cartesian.h>
#include <CGAL/Filtered_kernel.h>
#include <CGAL/Lazy_exact_nt.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>

#ifndef CGAL_KERNEL
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

void echo_segments() {
	for (const auto& seg : cgal_segments) {
		std::cout
		<< seg.start().x() << ";"
		<< seg.start().y() << ";"
		<< seg.end().x() << ";"
		<< seg.end().y()
		<< std::endl;
	}
}
