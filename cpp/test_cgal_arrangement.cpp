#include "utils_cgal.h"

typedef CGAL::Exact_predicates_exact_constructions_kernel K;

typedef K::Point_2 CGAL_Point;
typedef CGAL::Arr_segment_traits_2<K> CGAL_Traits;
typedef CGAL_Traits::Curve_2 CGAL_Segment;
typedef CGAL::Arrangement_2<CGAL_Traits> Arrangement;

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
    Arrangement arr;
    // Insert segments into the arrangement
    CGAL::insert(arr, cgal_segments.begin(), cgal_segments.end());

    // Count intersection points by counting arrangement vertices
    size_t intersection_points_count = 0;
    std::vector<std::pair<double, double>> intersection_points;
    for (auto vit = arr.vertices_begin(); vit != arr.vertices_end(); ++vit) {
        if (vit->degree() > 2) {  // Vertices with degree > 2 are intersection points
            intersection_points_count++;
            intersection_points.push_back(std::make_pair(
                CGAL::to_double(vit->point().x()), // Use CGAL's conversion
                CGAL::to_double(vit->point().y())  // Use CGAL's conversion
            ));
        }
    }

    return intersection_points_count;
}

size_t compute_print_crossings() {
    Arrangement arr;
    // Insert segments into the arrangement
    CGAL::insert(arr, cgal_segments.begin(), cgal_segments.end());

    // Count intersection points by counting arrangement vertices
    size_t intersection_points_count = 0;
    std::vector<std::pair<double, double>> intersection_points;
    for (auto vit = arr.vertices_begin(); vit != arr.vertices_end(); ++vit) {
        if (vit->degree() > 2) {  // Vertices with degree > 2 are intersection points
            intersection_points_count++;
            intersection_points.push_back(std::make_pair(
                CGAL::to_double(vit->point().x()), // Use CGAL's conversion
                CGAL::to_double(vit->point().y())  // Use CGAL's conversion
            ));
        }
    }

    for (const auto& point : intersection_points) {
        printBinary(point.first); // Print m_x as binary
        std::cout << ";"; // Separate with a semicolon
        printBinary(point.second); // Print m_y as binary
        std::cout << std::endl; // New line after each pair
    }

    return intersection_points_count;
}
