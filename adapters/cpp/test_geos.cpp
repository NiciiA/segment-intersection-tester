#include "utils.h"
#include <geos/algorithm/LineIntersector.h>
#include <geos/geom/Coordinate.h>
#include <geos/geom/CoordinateSequence.h>
#include <geos/geom/PrecisionModel.h>
#include <geos/noding/BasicSegmentString.h>
#include <geos/noding/MCIndexNoder.h>
#include <geos/noding/NodingIntersectionFinder.h>
#include <geos/noding/IntersectionFinderAdder.h>
#include <geos/noding/SimpleNoder.h>
#include <geos/version.h>


#if GEOS_VERSION_MINOR < 12
#	include <geos/geom/CoordinateArraySequence.h>
#	define CoordinateSequence CoordinateArraySequence
#endif

using namespace geos::geom;
using namespace geos::noding;
using namespace geos::algorithm;

std::vector<SegmentString*> segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2) {
	segments.push_back(new BasicSegmentString(
			new CoordinateSequence({Coordinate(bitstring_to_double(x1), bitstring_to_double(y1)),
					Coordinate(bitstring_to_double(x2), bitstring_to_double(y2))}), nullptr));
}

template<bool print>
size_t compute_crossings() {
	PrecisionModel pm(PrecisionModel::FLOATING);
	LineIntersector li(&pm);
	if (print) {
		std::vector<Coordinate> intersections;
		IntersectionFinderAdder ifa(li, intersections);
		SimpleNoder noder(&ifa);
		noder.computeNodes(&segments);
		for (const auto& coord : intersections) {
			print_point(coord.x, coord.y);
		}
		return intersections.size();
	} else {
		NodingIntersectionFinder ifa(li);
		ifa.setFindAllIntersections(true);
		SimpleNoder noder(&ifa);
		noder.computeNodes(&segments);
		return ifa.count() / 2;
	}

	// TODO other Noders?

	// // Cleanup
	// for (auto* seg : segments) {
	// 	delete seg->getCoordinates(); // since we manually allocated them
	// 	delete seg;
	// }
}

#include "main.hpp"
