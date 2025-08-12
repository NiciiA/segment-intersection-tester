#include "utils.h"
#include <geos/algorithm/LineIntersector.h>
#include <geos/geom/Coordinate.h>
#include <geos/geom/CoordinateSequence.h>
#include <geos/noding/BasicSegmentString.h>
#include <geos/noding/MCIndexNoder.h>
#include <geos/noding/SegmentIntersector.h>
#include <geos/noding/SegmentString.h>
#include <geos/noding/SimpleNoder.h>
#include <geos/version.h>

#if GEOS_VERSION_MINOR < 12
#	include <geos/geom/CoordinateArraySequence.h>
#	define CoordinateSequence CoordinateArraySequence
#endif

using namespace geos::geom;
using namespace geos::noding;
using namespace geos::algorithm;

class IntersectionCollector : public SegmentIntersector {
private:
	std::set<Coordinate> intersections;

	geos::geom::LineSegment getSegment(SegmentString* ss, std::size_t index) {
		const auto& p0 = ss->getCoordinate(index);
		const auto& p1 = ss->getCoordinate(index + 1);
		return geos::geom::LineSegment(p0, p1);
	}

public:
	void processIntersections(SegmentString* e0, std::size_t segIndex0, SegmentString* e1,
	                          std::size_t segIndex1) override {
		if (e0 == e1 && segIndex0 == segIndex1) {
			return;
		}

		LineSegment seg0 = getSegment(e0, segIndex0);
		LineSegment seg1 = getSegment(e1, segIndex1);

		LineIntersector li;
		li.computeIntersection(seg0.p0, seg0.p1, seg1.p0, seg1.p1);

		if (li.hasIntersection()) {
			for (int i = 0; i < li.getIntersectionNum(); ++i) {
				intersections.insert(li.getIntersection(i));
			}
		}
	}

	bool isDone() const override { return false; }

	const std::set<Coordinate>& getIntersections() const { return intersections; }
};

std::vector<SegmentString*> segments;

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
                  const std::string& y2) {
	segments.push_back(new BasicSegmentString(
		new CoordinateSequence({Coordinate(bitstring_to_double(x1), bitstring_to_double(y1)),
		                        Coordinate(bitstring_to_double(x2), bitstring_to_double(y2))}),
		nullptr));
}

void echo_segments() {
	for (const auto& s : segments) {
		std::cout
				<< s->getCoordinate(0).x << ";"
				<< s->getCoordinate(0).y << ";"
				<< s->getCoordinate(1).x << ";"
				<< s->getCoordinate(1).y
				<< std::endl;
	}
}

template<bool print>
size_t compute_crossings() {
	auto collector = std::make_unique<IntersectionCollector>();
	MCIndexNoder noder(collector.get());
	noder.computeNodes(&segments);

	const auto& coordinates = collector->getIntersections();
	if (print) {
		for (const auto& c : coordinates) {
			print_point(c.x, c.y);
		}
	}
	return coordinates.size();
}

#include "main.hpp"
