#include "utils.h"
#include <LEDA/graph/graph.h>

#ifdef RATIONAL

#	include <LEDA/geo/rat_kernel.h>
#	include <LEDA/geo/rat_kernel_names.h>
#	include <LEDA/geo/rat_geo_alg.h>

#	define PARSE(x) leda::rational(bitstring_to_double(x))

void print_point(const leda::rational& x, const leda::rational& y) {
	std::cout << x << ";" << y << std::endl;
}

#else // !RATIONAL

#	include <LEDA/geo/float_kernel.h>
#	include <LEDA/geo/float_kernel_names.h>
#	include <LEDA/geo/float_geo_alg.h>

#	define PARSE(x) bitstring_to_double(x)

#endif

using namespace leda;

list<SEGMENT> segments;
list<POINT> intersection_points;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
                  const std::string& y2) {
	segments.push_back(SEGMENT(POINT(PARSE(x1), PARSE(y1)), POINT(PARSE(x2), PARSE(y2))));
}

#ifdef RATIONAL
void echo_segments() {
	for (const auto& seg : segments) {
		auto start_x = seg.start().xcoord();
		auto start_y = seg.start().ycoord();
		auto end_x = seg.end().xcoord();
		auto end_y = seg.end().ycoord();
		start_x.normalize();
		start_y.normalize();
		end_x.normalize();
		end_y.normalize();
		std::cout
				<< (start_x.denominator() == 1
					? start_x.numerator().to_string()
					: start_x.to_string()) << ";"
				<< (start_y.denominator() == 1
					? start_y.numerator().to_string()
					: start_y.to_string()) << ";"
				<< (end_x.denominator() == 1
					? end_x.numerator().to_string()
					: end_x.to_string()) << ";"
				<< (end_y.denominator() == 1 ? end_y.numerator().to_string() : end_y.to_string())
				<< std::endl;
	}
}
#else
void echo_segments() {
	for (const auto& seg : segments) {
		std::cout
		<< seg.start().X() << ";"
		<< seg.start().Y() << ";"
		<< seg.end().X() << ";"
		<< seg.end().Y()
		<< std::endl;
	}
}
#endif


void check_intersection(const SEGMENT& a, const SEGMENT& b) {
#ifdef RATIONAL
	SEGMENT inter;
	if (a.intersection(b, inter)) {
		if (inter.is_trivial()) {
			intersection_points.push_back(inter.start());
		} else {
			intersection_points.push_back(inter.start());
			intersection_points.push_back(inter.end());
		}
	}
#else
	POINT inter;
	if (a.intersection(b, inter)) {
		intersection_points.push_back(inter);
	}
#endif
}

template<bool print>
size_t compute_crossings() {
#if defined(ALGO_REPORT)
	leda::ALGO(segments, check_intersection);
#elif defined(ALGO_GRAPH)
	GRAPH<POINT, SEGMENT> G;
	leda::ALGO(segments, G, false);
	node v;
	forall_nodes(v, G) if (G.degree(v) > 1)
		intersection_points.append(G[v]);
#else
	for (auto i = segments.first(); i; i = segments.succ(i)) {
		for (auto j = segments.succ(i); j; j = segments.succ(j)) {
			check_intersection(segments.contents(i), segments.contents(j));
		}
	}
#endif

	if (print) {
		for (const auto& p : intersection_points) {
			print_point(p.xcoord(), p.ycoord());
		}
	}
	return intersection_points.length();
}

#include "main.hpp"
