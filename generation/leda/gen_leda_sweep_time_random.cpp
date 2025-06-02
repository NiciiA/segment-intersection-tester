/*******************************************************************************
 * Simplified LEDA segment generator based on demo/sweep_time.cpp - RANDOM mode only
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

int main(int argc, char* argv[])
{
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <N> <k> <format>" << endl;
        cerr << "  N = number of segments" << endl;
        cerr << "  k = bit size for coordinates" << endl;
        cerr << "  format = 'integer' for integer output, 'double' for floating point" << endl;
        return 1;
    }
    
    int N = atoi(argv[1]);
    int k = atoi(argv[2]);
    std::string format = argv[3];
    
    if (N <= 0 || k <= 0) {
        cerr << "Error: N and k must be positive integers" << endl;
        return 1;
    }
    
    if (format != "integer" && format != "double") {
        cerr << "Error: format must be 'integer' or 'double'" << endl;
        return 1;
    }
    
    integer size = integer(1) << k;
    
    for(int i = 0; i < N; i++) {
        integer x1 = integer::random(k) - size;
        integer y1 = integer::random(k) - size;
        integer x2 = integer::random(k) - size;
        integer y2 = integer::random(k) - size;
        
        if (format == "integer") {
            // Output exact integers as strings
            cout << x1.to_string() << "," 
                 << y1.to_string() << "," 
                 << x2.to_string() << "," 
                 << y2.to_string() << endl;
        } else {
            // Convert to double first, identical to original's segment creation
            cout << x1.to_double() << "," 
                 << y1.to_double() << "," 
                 << x2.to_double() << "," 
                 << y2.to_double() << endl;
        }
    }
    
    return 0;
}
