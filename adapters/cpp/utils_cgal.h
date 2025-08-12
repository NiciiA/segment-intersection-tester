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

template<typename T = K::RT, std::enable_if_t<!std::is_same_v<T, double>, int> = 0>
void print_point(const T& x, const T& y) {
	std::cout << x << ";" << y << std::endl;
}

std::vector<CGAL_Segment> cgal_segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
                  const std::string& y2) {
	cgal_segments.emplace_back(
		CGAL_Segment(CGAL_Point(bitstring_to_double(x1), bitstring_to_double(y1)),
		             CGAL_Point(bitstring_to_double(x2), bitstring_to_double(y2))));
}

template<typename T>
void echo_segment(const T& s) {
	auto v = CGAL::exact(s.start());
	auto u = CGAL::exact(s.end());
	std::cout
			<< v.hx() / v.hw() << ";"
			<< v.hy() / v.hw() << ";"
			<< u.hx() / u.hw() << ";"
			<< u.hy() / u.hw()
			<< std::endl;
}

typedef CGAL::Segment_2<CGAL::Simple_cartesian<double>> DS;

void echo_segment(const DS& s) {
	std::cout
			<< s.source().hx() << ";"
			<< s.source().hy() << ";"
			<< s.target().hx() << ";"
			<< s.target().hy()
			<< std::endl;
}

void echo_segments() {
	for (const auto& seg : cgal_segments) {
		echo_segment(seg);
	}
}
