// for f in msc-graphstudy/data/layouts/**/*.xml.gz; do
//     d="$(basename $(dirname $f))-$(basename $f).csv"
//     if [[ -s $d ]]; then
//         echo "skipping $d"
//     else
//         echo "processing $d"
//         # python segment-intersection/generation/ogdf_converter.py $f > $d
//         segment-intersection/generation/leda/ogdf_to_segint $f > $d
//     fi
// done



#include <ogdf/basic/Graph.h>
#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/fileformats/GraphIO.h>

#include <boost/iostreams/filter/gzip.hpp>
#include <boost/iostreams/filtering_stream.hpp>

using namespace ogdf;
using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cerr << "Invalid argument count!" << endl;
        return 1;
    }

    // replace tsplib xml file type mapping by graphml
    GraphIO::getFileType("a.xml");
    GraphIO::FILE_TYPE_MAP.insert_or_assign("xml", GraphIO::FILE_TYPE_MAP.at("graphml"));

    Graph G;
    GraphAttributes GA(G, GraphAttributes::nodeGraphics);
    string file = argv[1];
    if (file.ends_with(".gz")) {
        auto ft = GraphIO::getFileType(file.substr(0, file.length() - 3));
        if (ft) {
            ifstream input(file);
            if (input.is_open()) {
                boost::iostreams::filtering_istream decompressedInput;
                decompressedInput.push(boost::iostreams::gzip_decompressor());
                decompressedInput.push(input);
                if (!ft->attr_reader_func(GA, G, decompressedInput)) {
                    cerr << "Failed to read compressed graph from file " << file << endl;
                    return 1;
                }
                input.close();
            } else {
                cerr << "Unable to open compressed file " << file << endl;
                return 1;
            }
        } else {
            cerr << "Failed to detect format within compressed file " << file << endl;
            return 1;
        }
    } else if (!GraphIO::read(GA, G, file)) {
        cerr << "Failed to read graph from file " << file << endl;
        return 1;
    }

    for (edge e : G.edges) {
        cout << GA.x(e->source()) << ";" << GA.y(e->source()) << ";" << GA.x(e->target()) << ";" << GA.y(e->target())
             << endl;
    }

    return 0;
}
