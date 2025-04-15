#pragma once

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
#include <string>
#include <bitset>
#include <stdexcept>


long getMemoryUsageKB() {
    task_basic_info info;
    mach_msg_type_number_t infoCount = TASK_BASIC_INFO_COUNT;
    if (task_info(mach_task_self(), TASK_BASIC_INFO, (task_info_t)&info, &infoCount) != KERN_SUCCESS) {
        return -1;
    }
    return info.resident_size;  // Convert bytes to KB
}

double bitstring_to_double(std::string s) {
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

void process_line(const std::string& line);

size_t compute_crossings();

size_t compute_print_crossings();

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

    std::string line;
    std::getline(file, line);

    while (std::getline(file, line)) {
        process_line(line);
    }

    file.close();

    long initial_memory = getMemoryUsageKB();
    auto start = std::chrono::high_resolution_clock::now();
    size_t num_crossings;
    if (print_intersections) {
      	std::cout << "p_x;p_y" << std::endl;
        num_crossings = compute_print_crossings();
    } else {
        num_crossings = compute_crossings();
    }
    auto end = std::chrono::high_resolution_clock::now();
    long final_memory = getMemoryUsageKB();

    if (!print_intersections) {
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
