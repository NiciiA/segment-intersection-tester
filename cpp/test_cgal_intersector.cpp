#include "utils_cgal.h"

typedef CGAL::Exact_predicates_exact_constructions_kernel K;

typedef K::Point_2 CGAL_Point;
typedef CGAL::Arr_segment_traits_2<K> CGAL_Traits;
typedef CGAL_Traits::Curve_2 CGAL_Segment;

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

    cgal_segments.emplace_back(CGAL_Segment(CGAL_Point(x1, y1), CGAL_Point(x2, y2)));
}

size_t compute_crossings() {
    std::list<CGAL_Point> pts;

    CGAL::compute_intersection_points(cgal_segments.begin(), cgal_segments.end(), std::back_inserter(pts), true);

    return pts.size();
}

size_t compute_print_crossings() {
    std::list<CGAL_Point> pts;

    CGAL::compute_intersection_points(cgal_segments.begin(), cgal_segments.end(), std::back_inserter(pts), false);

    for (const auto& point : pts) {
        double x = CGAL::to_double(point.x());
        double y = CGAL::to_double(point.y());

        printBinary(x); // Print m_x as binary
        std::cout << ";"; // Separate with a semicolon
        printBinary(y); // Print m_y as binary
        std::cout << std::endl; // New line after each pair
    }
}
