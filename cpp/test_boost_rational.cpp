//
// Created by Nicolas Ackermann on 10.10.2024.
//

#include <boost/geometry.hpp>
#include <boost/geometry/index/rtree.hpp>
#include <boost/rational.hpp>

#include <boost/multiprecision/gmp.hpp>  // Use GMP-backed multiprecision types

namespace bg = boost::geometry;
namespace bgi = bg::index;

namespace mp = boost::multiprecision;
using Rational = mp::mpq_rational;

typedef bg::model::point<Rational, 2, bg::cs::cartesian> Boost_Point;
typedef bg::model::linestring<Boost_Point> LineString;
typedef std::pair<LineString, unsigned> Value;

#include "utils_boost.h"

void process_line(const std::string& line) {
    std::stringstream ss(line);
    std::string token;

    double x1, y1, x2, y2;

    std::getline(ss, token, ';');
    // std::cout << "Token: " << token << std::endl;
    x1 = bitstring_to_double(token);
    // std::cout << "x1: " << x1 << std::endl;

    std::getline(ss, token, ';');
    // std::cout << "Token: " << token << std::endl;
    y1 = bitstring_to_double(token);
    // std::cout << "y1: " << y1 << std::endl;

    std::getline(ss, token, ';');
    // std::cout << "Token: " << token << std::endl;
    x2 = bitstring_to_double(token);
    // std::cout << "x2: " << x2 << std::endl;

    std::getline(ss, token, ';');
    // std::cout << "Token: " << token << std::endl;
    y2 = bitstring_to_double(token);
    // std::cout << "y2: " << y2 << std::endl;

    LineString lineString;
    bg::append(lineString, Boost_Point(Rational(x1), Rational(y1)));
    bg::append(lineString, Boost_Point(Rational(y2), Rational(y2)));
    boost_segments.push_back(lineString);
}
