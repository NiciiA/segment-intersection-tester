#include "utils_cgal.h"

#include <CGAL/Surface_sweep_2_algorithms.h>

template<bool print>
size_t compute_crossings() {
	std::list<CGAL_Point> pts;
	CGAL::compute_intersection_points(cgal_segments.begin(), cgal_segments.end(),
			std::back_inserter(pts), true);

	if (print) {
		for (const auto& point : pts) {
			print_point(CGAL::to_double(point.x()), CGAL::to_double(point.y()));
		}
	}

	return pts.size();
}

#include "main.hpp"
