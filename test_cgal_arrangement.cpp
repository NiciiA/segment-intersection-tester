//
// Created by Nicolas Ackermann on 10.10.2024.
//

#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include <vector>
#include <list>
#include <map>
#include <filesystem>
#include <sstream>
#include <utility>
#include <mach/mach.h>
#include <chrono>

#include <algorithm>
#include <cstring>
#include <bitset>
#include <stdexcept>

#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Surface_sweep_2_algorithms.h>
#include <CGAL/intersections.h>

typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef K::Point_2 CGAL_Point;
typedef CGAL::Arr_segment_traits_2<K> CGAL_Traits;
typedef CGAL_Traits::Curve_2 CGAL_Segment;

long getMemoryUsageKB() {
    task_basic_info info;
    mach_msg_type_number_t infoCount = TASK_BASIC_INFO_COUNT;
    if (task_info(mach_task_self(), TASK_BASIC_INFO, (task_info_t)&info, &infoCount) != KERN_SUCCESS) {
        return -1;
    }
    return info.resident_size;  // Convert bytes to KB
}

double bitstring_to_double(std::string s)
{
    s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char c) { return std::isspace(c); }), s.end());

    if (s.size() != 64) {
        throw std::invalid_argument("Invalid binary string: Must be 64 characters.");
    }

    unsigned long long x = 0;

    for (char c : s) {
        if (c != '0' && c != '1') {
            throw std::invalid_argument("Invalid binary string: Must contain only '0' and '1'.");
        }
        x = (x << 1) | (c - '0');
    }

    double d;
    std::memcpy(&d, &x, sizeof(d));
    return d;
}

void printBinary(double value) {
    uint64_t intRep;
    std::memcpy(&intRep, &value, sizeof(intRep)); // Treat the double as raw binary data
    std::bitset<64> binaryRep(intRep); // 64 bits for the double
    std::cout << binaryRep;
}

int main(int argc, char* argv[]) {
  	std::string file_path;
    bool print_intersections = false;
    int opt;

    while ((opt = getopt(argc, argv, "f:a")) != -1) {
        switch (opt) {
            case 'f':
                file_path = optarg;
                break;
            case 'a':
                print_intersections = true;
                break;
            default:
                std::cerr << "Usage: " << argv[0] << " -f <file_path>\n";
                return 1;
        }
    }

    std::vector<std::pair<std::pair<double, double>, std::pair<double, double>>> segment_points;

    if (file_path.empty()) {
        std::cerr << "Error: No file provided. Use -f <file_path> to specify a CSV file.\n";
        return 1;
    }

    if (file_path.substr(file_path.find_last_of(".") + 1) != "csv") {
        std::cerr << "Error: The specified file is not a .csv file.\n";
        return 1;
    }

    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << file_path << "\n";
        return 1;
    }

    // std::cout << "\n=== Testing file " << file_path << " ===" << std::endl;

    std::string line;
    std::getline(file, line);

    while (std::getline(file, line)) {
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

    file.close();

    std::vector<CGAL_Segment> cgal_segments;
    for (const auto& p : segment_points) {
        cgal_segments.emplace_back(CGAL_Segment(CGAL_Point(p.first.first, p.first.second), CGAL_Point(p.second.first, p.second.second)));
    }

    // std::cout << "\n--- CGAL Intersection Tests ---\n";

    std::list<CGAL_Point> pts;

    long initial_memory = getMemoryUsageKB();
    auto start = std::chrono::high_resolution_clock::now();

    CGAL::compute_intersection_points(cgal_segments.begin(), cgal_segments.end(), std::back_inserter(pts));

    auto end = std::chrono::high_resolution_clock::now();
    long final_memory = getMemoryUsageKB();

    if (print_intersections) {
      	std::cout << "p_x;p_y" << std::endl;
        for (const auto& point : pts) {
            double x = CGAL::to_double(point.x());
            double y = CGAL::to_double(point.y());

            printBinary(x); // Print m_x as binary
            std::cout << ";"; // Separate with a semicolon
            printBinary(y); // Print m_y as binary
            std::cout << std::endl; // New line after each pair
        }
    } else {
        std::cout << pts.size() << std::endl;

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << duration.count() << std::endl;

        if (initial_memory != -1 && final_memory != -1) {
            std::cout << (final_memory - initial_memory) << std::endl;
        } else {
            std::cout << "Failed to get memory usage" << std::endl;
        }
    }

    return 0;
}
