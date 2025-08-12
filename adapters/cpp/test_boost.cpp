#include "utils.h"

#include <boost/geometry.hpp>

namespace bg = boost::geometry;

#ifdef RATIONAL

#include <boost/multiprecision/gmp.hpp>

using Rational = boost::multiprecision::mpq_rational;
using Boost_Point = bg::model::point<Rational, 2, bg::cs::cartesian>;

#	define PARSE(x) Rational(bitstring_to_double(x))

void print_point(const Rational& x, const Rational& y) {
	std::cout << x << ";" << y << std::endl;
}

#else // !RATIONAL

using Boost_Point = bg::model::point<double, 2, bg::cs::cartesian>;

#	define PARSE(x) bitstring_to_double(x)

#endif

using LineString = bg::model::linestring<Boost_Point>;

std::vector<LineString> boost_segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2) {
	LineString lineString;
	bg::append(lineString, Boost_Point(PARSE(x1), PARSE(y1)));
	bg::append(lineString, Boost_Point(PARSE(x2), PARSE(y2)));
	boost_segments.push_back(lineString);
}

void echo_segments() {
	for (const auto& seg : boost_segments) {
		std::cout
		<< seg.front().get<0>() << ";"
		<< seg.front().get<1>() << ";"
		<< seg.back().get<0>() << ";"
		<< seg.back().get<1>()
		<< std::endl;
	}
}


template<bool print>
size_t compute_crossings() {
	size_t num_crossings = 0;

	std::deque<Boost_Point> output_points;
	for (size_t i = 0; i < boost_segments.size(); ++i) {
		for (size_t j = i + 1; j < boost_segments.size(); ++j) {
			output_points.clear();
			bg::intersection(boost_segments[i], boost_segments[j], output_points);
			num_crossings += output_points.size();

			if (print) {
				for (const auto& point : output_points) {
					print_point(bg::get<0>(point), bg::get<1>(point));
				}
			}
		}
	}

	return num_crossings;
}

#include "main.hpp"
