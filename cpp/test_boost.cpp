#include <boost/geometry.hpp>
#include <boost/geometry/index/rtree.hpp>

namespace bg = boost::geometry;
namespace bgi = bg::index;

namespace mp = boost::multiprecision;
using Rational = mp::mpq_rational;

typedef bg::model::point<double, 2, bg::cs::cartesian> Boost_Point;
typedef bg::model::linestring<Boost_Point> LineString;
typedef std::pair<LineString, unsigned> Value;

#include "utils_boost.h"

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

    LineString lineString;
    bg::append(lineString, Boost_Point(x1, y1));
    bg::append(lineString, Boost_Point(y2, y2));
    boost_segments.push_back(lineString);
}
