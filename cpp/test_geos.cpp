#include <iostream>
#include <vector>

#include <geos/geom/Coordinate.h>
#include <geos/geom/CoordinateSequence.h>
#include <geos/noding/BasicSegmentString.h>
#include <geos/noding/MCIndexNoder.h>

using namespace geos::geom;
using namespace geos::noding;

int main() {
	std::vector<SegmentString*> segments;

	// Segment 1: (0, 0) -> (2, 2)
	{
		auto* coords = new CoordinateSequence();
		coords->add(Coordinate(0, 0));
		coords->add(Coordinate(2, 2));
		segments.push_back(new BasicSegmentString(coords, nullptr));
	}

	// Segment 2: (0, 2) -> (2, 0)
	{
		auto* coords = new CoordinateSequence();
		coords->add(Coordinate(0, 2));
		coords->add(Coordinate(2, 0));
		segments.push_back(new BasicSegmentString(coords, nullptr));
	}

	// Run the MCIndexNoder to find intersections
	MCIndexNoder noder;
	std::cout << "Calling computeNodes...\n";
	noder.computeNodes(&segments);
	std::cout << "Done.\n";

	const auto* noded = noder.getNodedSubstrings();
	for (const auto& seg : *noded) {
		const CoordinateSequence* coords = seg->getCoordinates();
		std::cout << "Segment: ";
		for (std::size_t i = 0; i < coords->size(); ++i) {
			auto c = coords->getAt(i);
			std::cout << "(" << c.x << ", " << c.y << ") ";
		}
		std::cout << "\n";
	}

	// Cleanup
	for (auto* seg : segments) {
		delete seg->getCoordinates(); // since we manually allocated them
		delete seg;
	}

	return 0;
}
