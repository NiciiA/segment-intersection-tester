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
#include <set>

#include <algorithm>
#include <cstring>
#include <bitset>
#include <stdexcept>


#include <ogdf/basic/Graph.h>
#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/basic/graph_generators.h>
#include <ogdf/basic/LayoutStatistics.h>

using namespace ogdf;

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

    // std::cout << "\n--- OGDF Intersection Tests ---\n";

    Graph IG;
    NodeArray<DPoint> edgeMapping;       // Maps nodes in H to their geometric positions
    NodeArray<node> origNode;          // Maps nodes in H to nodes in the original graph (or nullptr)
    EdgeArray<edge> origEdge;

    long initial_memory = getMemoryUsageKB();
    auto start = std::chrono::high_resolution_clock::now();

    ArrayBuffer<int> crossings = LayoutStatistics::numberOfCrossings(GA);

    auto end = std::chrono::high_resolution_clock::now();
    long final_memory = getMemoryUsageKB();

    // std::cout << "OGDF: Found the following edge crossings:\n";

    int num_crossings = 0;
    for (int i = 0; i < crossings.size(); ++i) {
        num_crossings += crossings[i];
    }

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    if (print_intersections) {
      	std::cout << "p_x;p_y" << std::endl;
        LayoutStatistics::intersectionGraph(GA, IG, edgeMapping, origNode, origEdge);
        for (const auto& point : edgeMapping) {
            if (endpointPositions.find(point) == endpointPositions.end()) {
                printBinary(point.m_x); // Print m_x as binary
                std::cout << ";"; // Separate with a semicolon
                printBinary(point.m_y); // Print m_y as binary
                std::cout << std::endl; // New line after each pair
            }
        }
    } else {
        std::cout << num_crossings / 2 << std::endl;
        std::cout << duration.count() << std::endl;

        if (initial_memory != -1 && final_memory != -1) {
            std::cout << (final_memory - initial_memory) << std::endl;
        } else {
            std::cout << "Failed to get memory usage" << std::endl;
        }
    }

    return 0;
}
