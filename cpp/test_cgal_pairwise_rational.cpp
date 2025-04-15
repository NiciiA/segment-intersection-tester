#include "utils_cgal.h"

#include <CGAL/Object.h>
#include <CGAL/Exact_rational.h>
#include <CGAL/number_utils.h>
#include <CGAL/to_rational.h>

typedef CGAL::Exact_rational NT;
typedef CGAL::Cartesian<NT> K;

typedef K::Point_2 CGAL_Point;
typedef CGAL::Arr_segment_traits_2<K> CGAL_Traits;
typedef CGAL_Traits::Segment_2 CGAL_Segment;

std::vector<CGAL_Segment> cgal_segments;

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

    cgal_segments.emplace_back(CGAL_Segment(CGAL_Point(CGAL::to_rational<NT>(x1), CGAL::to_rational<NT>(y1)), CGAL_Point(CGAL::to_rational<NT>(x2), CGAL::to_rational<NT>(y2))));
}

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

    return pts.size();
}

size_t compute_print_crossings() {
    std::set<CGAL_Point> pts;

    for (size_t i = 0; i < cgal_segments.size(); ++i) {
        for (size_t j = i + 1; j < cgal_segments.size(); ++j) {
            CGAL::Object result = CGAL::intersection(cgal_segments[i], cgal_segments[j]);
            CGAL_Point ipoint;
            CGAL_Segment iseg;

            if (CGAL::assign(ipoint, result)) {
                pts.insert(ipoint);
            } else if (CGAL::assign(iseg, result)) {
                pts.insert(iseg.source());
                pts.insert(iseg.target());
            }
        }
    }

    for (const auto& point : pts) {
        double x = CGAL::to_double(point.x());
        double y = CGAL::to_double(point.y());

        printBinary(x);
        std::cout << ";";
        printBinary(y);
        std::cout << std::endl;
    }

    return pts.size();
}