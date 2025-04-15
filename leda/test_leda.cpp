#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <unistd.h>  // for getopt
#include <sys/resource.h>  // for memory usage
#include <LEDA/graph/graph.h>
#include <LEDA/geo/segment.h>
#include <LEDA/geo/point.h>
#include <LEDA/geo/float_geo_alg.h>

#include <algorithm>
#include <cstring>
#include <bitset>
#include <stdexcept>

long getMemoryUsageKB() {
    struct rusage usage;
    if (getrusage(RUSAGE_SELF, &usage) != 0) {
        return -1;
    }
    return usage.ru_maxrss * 1024;  // Memory usage in Bytes
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

    // Parse command-line arguments
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

    // Verify file path
    if (file_path.empty()) {
        std::cerr << "Error: No file provided. Use -f <file_path> to specify a CSV file.\n";
        return 1;
    }

    if (file_path.substr(file_path.find_last_of(".") + 1) != "csv") {
        std::cerr << "Error: The specified file is not a .csv file.\n";
        return 1;
    }

    // Read CSV file for segment points
    leda::list<leda::segment> segments;
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << file_path << "\n";
        return 1;
    }

    std::string line;
    std::getline(file, line); // Skip header line
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

        segments.push_back(leda::segment(leda::point(x1, y1), leda::point(x2, y2)));
    }
    file.close();

    // Measure memory usage and time
    long initial_memory = getMemoryUsageKB();
    auto start = std::chrono::steady_clock::now();

    leda::list<leda::point> intersection_points;
    leda::SEGMENT_INTERSECTION(segments, intersection_points);

    auto end = std::chrono::steady_clock::now();
    long final_memory = getMemoryUsageKB();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    if (print_intersections) {
        std::cout << "p_x;p_y" << std::endl;
        for (const leda::point& p : intersection_points) {
            printBinary(p.xcoord()); // Print m_x as binary
            std::cout << ";"; // Separate with a semicolon
            printBinary(p.ycoord()); // Print m_y as binary
            std::cout << std::endl; // New line after each pair
        }
    } else {
        std::cout << intersection_points.length() << std::endl;

        std::cout << duration.count() << std::endl;

        if (initial_memory != -1 && final_memory != -1) {
            std::cout << (final_memory - initial_memory) << std::endl;
        } else {
            std::cout << "Failed to get memory usage" << std::endl;
        }
    }

    return 0;
}
