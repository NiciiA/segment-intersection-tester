#include "utils.h"

#include <LEDA/graph/graph.h>
#include <LEDA/geo/rat_segment.h>
#include <LEDA/geo/rat_point.h>
#include <LEDA/numbers/rational.h>
#include <LEDA/geo/rat_geo_alg.h>

#include <LEDA/core/set.h>

#include <set>

std::vector<leda::rat_segment> segments;

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

    segments.emplace_back(leda::rat_segment(leda::rat_point(leda::rational(x1), leda::rational(y1)), leda::rat_point(leda::rational(x2), leda::rational(y2))));
}

size_t compute_crossings() {
    leda::set<leda::rat_point> intersection_points;

    for (size_t i = 0; i < segments.size(); ++i) {
        for (size_t j = i + 1; j < segments.size(); ++j) {
            leda::rat_point inter;
            if (segments[i].intersection(segments[j], inter)) {
                intersection_points.insert(inter);
            }
        }
    }

    return static_cast<size_t>(intersection_points.size());
}

size_t compute_print_crossings() {
    leda::set<leda::rat_point> intersection_points;

    for (size_t i = 0; i < segments.size(); ++i) {
        for (size_t j = i + 1; j < segments.size(); ++j) {
            leda::rat_point inter;
            if (segments[i].intersection(segments[j], inter)) {
                intersection_points.insert(inter);
            }
        }
    }

    for (const leda::rat_point& p : intersection_points) {
        printBinary(p.xcoord().to_double()); // Print m_x as binary
        std::cout << ";"; // Separate with a semicolon
        printBinary(p.ycoord().to_double()); // Print m_y as binary
        std::cout << std::endl; // New line after each pair
    }

    return static_cast<size_t>(intersection_points.size());
}