/*******************************************************************************
 * Simplified LEDA segment generator based on demo/geo/sweep_intersection_time.cpp
 * Outputs segments as CSV: x1,y1,x2,y2
 *******************************************************************************/

#include <LEDA/numbers/integer.h>
#include <iostream>
#include <cstdlib>
#include <string>

using namespace leda;
using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char* argv[]) {

    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <N> <k> <s> " << endl;
        cerr << "  N = number of segments" << endl;
        cerr << "  k = bit size for coordinates" << endl;
        cerr << "  s = perturbation parameter (0 = all segments pass through origin)" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    int k = atoi(argv[2]);
    int s = atoi(argv[3]);

    if (N <= 0 || k <= 0 || s < 0) {
        cerr << "Error: N and k must be positive, s must be non-negative" << endl;
        return 1;
    }
    
    integer size = integer(1) << k;
    integer y = size;
    integer d = (N <= 1 ? size : 2 * size / (N - 1));

    cout << "x1;y1;x2;y2" << endl;

    for (s = k - 8; s <= k; s++) {
	// list<rat_segment> seglist;

	// integer size = integer(1) << k;
	// integer S    = integer(1) << s;

	for(int i=0; i < N; i++) {
	  integer x1 = integer::random(k);
	  integer y1 = integer::random(k);
	  integer w1 = 1;
	  integer x2 = x1 + integer::random(s);
	  integer y2 = y1 + integer::random(s);
	  integer w2 = 1;

	  // rat_segment s(rat_point(x1,y1,w1),rat_point(x2,y2,w2));
	  // seglist.append(s);

	  cout << x1.to_string() << ";" 
	       << y1.to_string() << ";" 
	       << x2.to_string() << ";" 
	       << y2.to_string() << endl;
	}
    }
    
    return 0;
}
