#include "utils.h"

#include <ogdf/basic/Graph.h>
#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/basic/LayoutStatistics.h>
#include <ogdf/basic/graph_generators.h>

using namespace ogdf;

Graph G;
GraphAttributes GA(G, GraphAttributes::nodeGraphics | GraphAttributes::edgeGraphics);

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2) {
	node n1 = G.newNode();
	GA.x(n1) = bitstring_to_double(x1);
	GA.y(n1) = bitstring_to_double(y1);
	node n2 = G.newNode();
	GA.x(n2) = bitstring_to_double(x2);
	GA.y(n2) = bitstring_to_double(y2);
	G.newEdge(n1, n2);
}

template<>
size_t compute_crossings<false>() {
	ArrayBuffer<int> crossings = LayoutStatistics::numberOfCrossings(GA);
	size_t num_crossings = 0;
	for (int i = 0; i < crossings.size(); ++i) {
		num_crossings += crossings[i];
	}
	return num_crossings / 2;
}

template<>
size_t compute_crossings<true>() {
	Graph IG;
	NodeArray<DPoint> edgeMapping;
	NodeArray<node> origNode;
	EdgeArray<edge> origEdge;
	size_t count = 0;

	LayoutStatistics::intersectionGraph(GA, IG, edgeMapping, origNode, origEdge);
	for (node n : IG.nodes) {
		if (!origNode[n]) {
			++count;
			auto point = edgeMapping[n];
			print_point(point.m_x, point.m_y);
		}
	}

	return count;
}

#include "main.hpp"
