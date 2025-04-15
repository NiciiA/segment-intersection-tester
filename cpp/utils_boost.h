#pragma once

#include "utils.h"

#include <string>

std::vector<LineString> boost_segments;

size_t compute_crossings() {
    size_t num_crossings = 0;

    for (size_t i = 0; i < boost_segments.size(); ++i) {
        for (size_t j = i + 1; j < boost_segments.size(); ++j) {
            std::deque<Boost_Point> output_points;

            bg::intersection(boost_segments[i], boost_segments[j], output_points);

            num_crossings += output_points.size();
        }
    }

    return num_crossings;
}

size_t compute_print_crossings() {
    size_t num_crossings = 0;

    for (size_t i = 0; i < boost_segments.size(); ++i) {
        for (size_t j = i + 1; j < boost_segments.size(); ++j) {
            std::deque<Boost_Point> output_points;

            bg::intersection(boost_segments[i], boost_segments[j], output_points);

            num_crossings += output_points.size();

            for (const auto& point : output_points) {
                auto coord_x = bg::get<0>(point);
                auto coord_y = bg::get<1>(point);

                printBinary(static_cast<double>(coord_x)); // Print m_x as binary
                std::cout << ";"; // Separate with a semicolon
                printBinary(static_cast<double>(coord_y)); // Print m_y as binary
                std::cout << std::endl; // New line after each pair
            }
        }
    }

    return num_crossings;
}
