#include "utils.h"

#include <set>

#include <ogdf/basic/Graph.h>
#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/basic/graph_generators.h>
#include <ogdf/basic/LayoutStatistics.h>

using namespace ogdf;

std::vector<std::pair<std::pair<double, double>, std::pair<double, double>>> segment_points;

void process_line(const std::string& line) {
    std::stringstream ss(line);
    std::string token;

    double x1, y1, x2, y2;

    std::getline(ss, token, ';');
    x1 = bitstring_to_double(token);

    std::getline(ss, token, ';');
    y1 = bitstring_to_double(token);

    std::getline(ss, token, ';');
    x2 = bitstring_to_double(token);

    std::getline(ss, token, ';');
    y2 = bitstring_to_double(token);

    segment_points.push_back({{x1, y1}, {x2, y2}});
}

size_t compute_crossings() {
    ogdf::Graph G;
    ogdf::GraphAttributes GA(G, GraphAttributes::nodeGraphics | GraphAttributes::edgeGraphics);

    std::map<std::pair<double, double>, node> point_to_node;

    std::set<DPoint> endpointPositions;

    for (const auto& segment : segment_points) {
        std::pair<double, double> p1 = segment.first;
        std::pair<double, double> p2 = segment.second;

        node n1, n2;
        DPoint d1(p1.first, p1.second);
        DPoint d2(p2.first, p2.second);

        if (point_to_node.find(p1) == point_to_node.end()) {
            n1 = G.newNode();
            GA.x(n1) = p1.first;
            GA.y(n1) = p1.second;
            point_to_node[p1] = n1;
            endpointPositions.insert(d1);
        } else {
            n1 = point_to_node[p1];
        }

        if (point_to_node.find(p2) == point_to_node.end()) {
            n2 = G.newNode();
            GA.x(n2) = p2.first;
            GA.y(n2) = p2.second;
            point_to_node[p2] = n2;
            endpointPositions.insert(d2);
        } else {
            n2 = point_to_node[p2];
        }

        G.newEdge(n1, n2);
    }

    Graph IG;
    NodeArray<DPoint> edgeMapping;       // Maps nodes in H to their geometric positions
    NodeArray<node> origNode;          // Maps nodes in H to nodes in the original graph (or nullptr)
    EdgeArray<edge> origEdge;

    ArrayBuffer<int> crossings = LayoutStatistics::numberOfCrossings(GA);

    size_t num_crossings = 0;
    for (int i = 0; i < crossings.size(); ++i) {
        num_crossings += crossings[i];
    }

    return num_crossings / 2;
}

size_t compute_print_crossings() {
    ogdf::Graph G;
    ogdf::GraphAttributes GA(G, GraphAttributes::nodeGraphics | GraphAttributes::edgeGraphics);

    std::map<std::pair<double, double>, node> point_to_node;

    std::set<DPoint> endpointPositions;

    for (const auto& segment : segment_points) {
        std::pair<double, double> p1 = segment.first;
        std::pair<double, double> p2 = segment.second;

        node n1, n2;
        DPoint d1(p1.first, p1.second);
        DPoint d2(p2.first, p2.second);

        if (point_to_node.find(p1) == point_to_node.end()) {
            n1 = G.newNode();
            GA.x(n1) = p1.first;
            GA.y(n1) = p1.second;
            point_to_node[p1] = n1;
            endpointPositions.insert(d1);
        } else {
            n1 = point_to_node[p1];
        }

        if (point_to_node.find(p2) == point_to_node.end()) {
            n2 = G.newNode();
            GA.x(n2) = p2.first;
            GA.y(n2) = p2.second;
            point_to_node[p2] = n2;
            endpointPositions.insert(d2);
        } else {
            n2 = point_to_node[p2];
        }

        G.newEdge(n1, n2);
    }

    Graph IG;
    NodeArray<DPoint> edgeMapping;       // Maps nodes in H to their geometric positions
    NodeArray<node> origNode;          // Maps nodes in H to nodes in the original graph (or nullptr)
    EdgeArray<edge> origEdge;

    ArrayBuffer<int> crossings = LayoutStatistics::numberOfCrossings(GA);

    size_t num_crossings = 0;
    for (int i = 0; i < crossings.size(); ++i) {
        num_crossings += crossings[i];
    }

    LayoutStatistics::intersectionGraph(GA, IG, edgeMapping, origNode, origEdge);
    for (const auto& point : edgeMapping) {
        if (endpointPositions.find(point) == endpointPositions.end()) {
            printBinary(point.m_x); // Print m_x as binary
            std::cout << ";"; // Separate with a semicolon
            printBinary(point.m_y); // Print m_y as binary
            std::cout << std::endl; // New line after each pair
        }
    }

    return num_crossings / 2;
}
