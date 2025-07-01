/*******************************************************************************
 * LEDA segment generator based on demo/d2_geo/intersect_circle_segments.cpp
 * Outputs segments as CSV: x1,y1,x2,y2
 *******************************************************************************/
#include <LEDA/numbers/integer.h>
#include <LEDA/geo/plane_alg.h>        // Required for polygon, circle, etc.
#include <LEDA/geo/r_circle_segment.h> // Required for r_circle_segment
#include <iostream>
#include <cstdlib>
#include <string>
using namespace leda;
using std::cerr;
using std::cout;
using std::endl;
typedef r_circle_segment SEGMENT;
static list<SEGMENT> seglist;

void add_curved_polygon(const polygon& poly, list<SEGMENT>& seglist)
{
  segment _s;
  forall_segments(_s, poly) {
    rat_segment s(_s);
    rat_point middle = s.source() + (s.target() - s.source()) / 2;
    rat_segment rot = s.rotate90(middle);
    r_circle_segment cs(s.source(), rot.source(), s.target());
    seglist.append(cs);
  }
}

void gen_ngon(list<SEGMENT>& seglist, int N, double radius)
{
  seglist.clear();
  circle C(point(radius,0), point(0,radius), point(-radius,0));
  polygon poly = n_gon(N, C, radius/1024);
  add_curved_polygon(poly, seglist);
  add_curved_polygon(poly.rotate(LEDA_PI/(2*N)), seglist);
}

int main(int argc, char* argv[])
{
    if (argc < 2 || argc > 3) {
        cerr << "Usage: " << argv[0] << " <N> [radius]" << endl;
        cerr << "  N = number of polygon vertices" << endl;
        cerr << "  radius = polygon radius (default: 800.0)" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    double radius = 800.0;  // default value
    
    if (argc == 3) {
        radius = atof(argv[2]);
    }
    
    if (N <= 0) {
        cerr << "Error: N must be a positive integer" << endl;
        return 1;
    }
    
    if (radius <= 0.0) {
        cerr << "Error: radius must be positive" << endl;
        return 1;
    }
    
    gen_ngon(seglist, N, radius);
    cout << "x1;y1;x2;y2" << endl;
    
    SEGMENT s;
    forall(s, seglist) {
      rat_segment t = s.to_rat_segment();
      cout << t.xcoord1D() << ";" << t.ycoord1D() << ";" 
           << t.xcoord2D() << ";" << t.ycoord2D() << endl;
    }
    
    return 0;
}
