#pragma once

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>

#include <unistd.h>

#if __APPLE__
#	include <mach/mach.h>

long getMemoryUsageKB() {
	task_basic_info info;
	mach_msg_type_number_t infoCount = TASK_BASIC_INFO_COUNT;
	if (task_info(mach_task_self(), TASK_BASIC_INFO, (task_info_t)&info, &infoCount) != KERN_SUCCESS) {
		return -1;
	}
	return info.resident_size;
}
#else
#	include <sys/resource.h>

long getMemoryUsageKB() {
	struct rusage usage;
	if (getrusage(RUSAGE_SELF, &usage) != 0) {
		return -1;
	}
	return usage.ru_maxrss * 1024;
}
#endif

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
		std::cerr << "Error: No file provided. Use -f <file_path> to specify a CSV "
					 "file.\n";
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
	while (!line.empty() && std::isspace(line.front())) line.erase(0, 1);
	while (!line.empty() && std::isspace(line.back())) line.pop_back();
	if (line != "x1;y1;x2;y2") {
		std::cerr << "Invalid header in file " << file_path << ":\n'" << line << "'" << std::endl;
		return 1;
	}
	while (std::getline(file, line)) {
		process_line(line);
	}

	file.close();

	long initial_memory = getMemoryUsageKB();
	auto start = std::chrono::high_resolution_clock::now();
	size_t num_crossings;
	if (print_intersections) {
		std::cout << "p_x;p_y" << std::endl;
		num_crossings = compute_crossings<true>();
	} else {
		num_crossings = compute_crossings<false>();
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
