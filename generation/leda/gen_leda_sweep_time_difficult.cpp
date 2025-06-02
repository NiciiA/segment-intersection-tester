/*******************************************************************************
 * Simplified LEDA segment generator based on demo/sweep_time.cpp - DIFFI mode only
 * Outputs segments as CSV: x1,y1,x2,y2
 * Creates segments that intersect near origin when s=0
 *******************************************************************************/

#include <LEDA/numbers/integer.h>
#include <iostream>
#include <cstdlib>
#include <string>

using namespace leda;
using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char* argv[])
{
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " <N> <k> <s> <format>" << endl;
        cerr << "  N = number of segments" << endl;
        cerr << "  k = bit size for coordinates" << endl;
        cerr << "  s = perturbation parameter (0 = all segments pass through origin)" << endl;
        cerr << "  format = 'integer' for integer output, 'double' for floating point" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    int k = atoi(argv[2]);
    int s = atoi(argv[3]);
    std::string format = argv[4];
    
    if (N <= 0 || k <= 0 || s < 0) {
        cerr << "Error: N and k must be positive, s must be non-negative" << endl;
        return 1;
    }
    
    if (format != "integer" && format != "double") {
        cerr << "Error: format must be 'integer' or 'double'" << endl;
        return 1;
    }
    
    integer size = integer(1) << k;
    integer y = size;
    integer d = (N <= 1 ? size : 2 * size / (N - 1));

    cout << "x1;y1;x2;y2" << endl;
    
    for(int i = 0; i < N; i++) {
        // Identical generation logic as original DIFFI mode
        integer x1 = size + rand_int(-s, s);
        integer y1 = size + y + rand_int(-s, s);
        integer x2 = 3*size + rand_int(-s, s);
        integer y2 = 3*size - y + rand_int(-s, s);
        
        // Increment y for next iteration
        y += d;
        
        if (format == "integer") {
            // Output exact integers as strings
            cout << x1.to_string() << ";" 
                 << y1.to_string() << ";" 
                 << x2.to_string() << ";" 
                 << y2.to_string() << endl;
        } else {
            // Convert to double first, identical to original's segment creation
            cout << x1.to_double() << ";" 
                 << y1.to_double() << ";" 
                 << x2.to_double() << ";" 
                 << y2.to_double() << endl;
        }
    }
    
    return 0;
}
