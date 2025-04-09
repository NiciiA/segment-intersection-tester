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

#include <boost/geometry.hpp>
#include <boost/rational.hpp>
#include <boost/geometry/index/rtree.hpp>

#include <boost/multiprecision/gmp.hpp>  // Use GMP-backed multiprecision types

namespace bg = boost::geometry;
namespace bgi = bg::index;

namespace mp = boost::multiprecision;
using Rational = mp::mpq_rational;

typedef bg::model::point<Rational, 2, bg::cs::cartesian> Boost_Point;
typedef bg::model::linestring<Boost_Point> LineString;
typedef std::pair<LineString, unsigned> Value;

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

    std::vector<std::pair<std::pair<long long, long long>, std::pair<long long, long long>>> segment_points;

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

    //std::cout << "\n=== Testing file " << file_path << " ===" << std::endl;

    std::string line;
    std::getline(file, line);

    std::vector<LineString> boost_segments;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string token;

        __int128 x1n, x1d, y1n, y1d, x2n, x2d, y2n, y2d;

        // Read and convert the first token (x1n, x1d)
        std::getline(ss, token, ';');
        std::stringstream(token) >> x1n;
        std::getline(ss, token, ';');
        std::stringstream(token) >> x1d;

        // Read and convert the second token (y1n, y1d)
        std::getline(ss, token, ';');
        std::stringstream(token) >> y1n;
        std::getline(ss, token, ';');
        std::stringstream(token) >> y1d;

        // Read and convert the third token (x2n, x2d)
        std::getline(ss, token, ';');
        std::stringstream(token) >> x2n;
        std::getline(ss, token, ';');
        std::stringstream(token) >> x2d;

        // Read and convert the fourth token (y2n, y2d)
        std::getline(ss, token, ';');
        std::stringstream(token) >> y2n;
        std::getline(ss, token, ';');
        std::stringstream(token) >> y2d;


        LineString line;
        bg::append(line, Boost_Point(Rational(x1n, x1d), Rational(y1n, y1d)));
        bg::append(line, Boost_Point(Rational(x2n, x2d), Rational(y2n, y2d)));
        boost_segments.push_back(line);
    }

    file.close();

    //std::cout << "\n--- Boost.Geometry Intersection Tests ---\n";

    int num_crossings = 0;

    long initial_memory = getMemoryUsageKB();
    auto start = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < boost_segments.size(); ++i) {
        for (size_t j = i + 1; j < boost_segments.size(); ++j) {
            if (bg::intersects(boost_segments[i], boost_segments[j])) {
                num_crossings++;
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    long final_memory = getMemoryUsageKB();

    num_crossings = 0;

    for (size_t i = 0; i < boost_segments.size(); ++i) {
        	for (size_t j = i + 1; j < boost_segments.size(); ++j) {
                std::deque<LineString> output_lines;
                std::deque<Boost_Point> output_points;

                // Get intersections as points or lines
                bg::intersection(boost_segments[i], boost_segments[j], output_lines);

                // Print LineString intersections
                for (const auto& line : output_lines) {
                    if (line.size() == 1 || (bg::get<0>(line.front()) == bg::get<0>(line.back()) && bg::get<1>(line.front()) == bg::get<1>(line.back()))) {
        				// Increment by 1 if it's a point
        				num_crossings += 1;
    				} else {
        				// Increment by 2 if it's a line
        				num_crossings += 2;
    				}
                }
        	}
    	}

    if (print_intersections) {
      	std::cout << "p_x;p_y" << std::endl;

        for (size_t i = 0; i < boost_segments.size(); ++i) {
        	for (size_t j = i + 1; j < boost_segments.size(); ++j) {
                std::deque<LineString> output_lines;
                std::deque<Boost_Point> output_points;

                // Get intersections as points or lines
                bg::intersection(boost_segments[i], boost_segments[j], output_points);

                // Print LineString intersections
                for (const auto& line : output_lines) {
                }
                for (const auto& point : output_points) {
                    auto coord_x = bg::get<0>(point);
                    auto coord_y = bg::get<1>(point);

                    std::cout << coord_x;
                	std::cout << ";"; // Separate with a semicolon
                    std::cout << coord_y;
                	std::cout << std::endl; // New line after each pair
                }
        	}
    	}
    } else {
    	std::cout << num_crossings << std::endl;

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
