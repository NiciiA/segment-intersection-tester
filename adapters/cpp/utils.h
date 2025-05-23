#pragma once

#include <algorithm>
#include <bitset>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <unistd.h>

double bitstring_to_double(std::string s) {
	s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char c) { return std::isspace(c); }),
			s.end());

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

void print_binary(double value) {
	uint64_t intRep;
	std::memcpy(&intRep, &value, sizeof(intRep)); // Treat the double as raw binary data
	std::bitset<64> binaryRep(intRep); // 64 bits for the double
	std::cout << binaryRep;
}

void print_point(double x, double y) {
	print_binary(x);
	std::cout << ";";
	print_binary(y);
	std::cout << std::endl;
}

void process_line(const std::string& x1, const std::string& y1, const std::string& x2,
		const std::string& y2);

void process_line(const std::string& line) {
	std::stringstream ss(line);
	std::string x1, y1, x2, y2;
	std::getline(ss, x1, ';');
	std::getline(ss, y1, ';');
	std::getline(ss, x2, ';');
	std::getline(ss, y2, ';');
	process_line(x1, y1, x2, y2);
}

template<bool print>
size_t compute_crossings();
