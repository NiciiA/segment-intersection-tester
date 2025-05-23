#include "utils_cgal.h"

#include <set>

#include <CGAL/Object.h>
#include <CGAL/intersections.h>
#include <CGAL/Arrangement_2.h>

template<bool print>
size_t compute_crossings() {
	std::set<CGAL_Point> pts;

	for (size_t i = 0; i < cgal_segments.size(); ++i) {
		for (size_t j = i + 1; j < cgal_segments.size(); ++j) {
			CGAL::Object result = CGAL::intersection(cgal_segments[i], cgal_segments[j]);
			CGAL_Point ipoint;
			CGAL_Segment iseg;

			if (CGAL::assign(ipoint, result)) {
				pts.insert(ipoint);
			} else if (CGAL::assign(iseg, result)) {
				// Insert both endpoints of the overlapping segment
				pts.insert(iseg.source());
				pts.insert(iseg.target());
			}
		}
	}

	if (print) {
		for (const auto& point : pts) {
			print_point(CGAL::to_double(point.x()), CGAL::to_double(point.y()));
		}
	}

	return pts.size();
}

#include "main.hpp"
