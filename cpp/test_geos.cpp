#include "utils.h"
#include <geos/algorithm/LineIntersector.h>
#include <geos/geom/Coordinate.h>
#include <geos/geom/CoordinateSequence.h>
#include <geos/noding/BasicSegmentString.h>
#include <geos/noding/MCIndexNoder.h>
#include <geos/noding/IntersectionFinderAdder.h>
#include <geos/noding/NodingIntersectionFinder.h>
#include <geos/noding/SimpleNoder.h>

using namespace geos::geom;
using namespace geos::noding;
using namespace geos::algorithm;

std::vector<SegmentString*> segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2) {
	segments.push_back(new BasicSegmentString(nullptr,
			new CoordinateSequence({Coordinate(bitstring_to_double(x1), bitstring_to_double(y1)),
					Coordinate(bitstring_to_double(x2), bitstring_to_double(y2))})));
}

template<bool print>
size_t compute_crossings() {
	PrecisionModel pm(PrecisionModel::FLOATING);
	LineIntersector li(&pm);
	NodingIntersectionFinder ifa(li);
	ifa.setFindAllIntersections(true);
	SimpleNoder noder(&ifa);
	noder.computeNodes(&segments);
	return ifa.count() / 2;

	// TODO test other noding strategies
	// FIXME needed for print=true, but requires NodedSegmentStrings
	// std::vector<Coordinate > intersections;
	// IntersectionFinderAdder  ifa(li, intersections);
	// const auto* noded = noder.getNodedSubstrings();
	// for (const auto& seg : *noded) {
	// 	const CoordinateSequence* coords = seg->getCoordinates();
	// 	std::cout << "Segment: ";
	// 	for (std::size_t i = 0; i < coords->size(); ++i) {
	// 		auto c = coords->getAt(i);
	// 		std::cout << "(" << c.x << ", " << c.y << ") ";
	// 	}
	// 	std::cout << "\n";
	// }
	//
	// // Cleanup
	// for (auto* seg : segments) {
	// 	delete seg->getCoordinates(); // since we manually allocated them
	// 	delete seg;
	// }
}

#include "main.hpp"
