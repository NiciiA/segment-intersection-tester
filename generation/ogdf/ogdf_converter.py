import click
from ogdf_python import *

# this implementation is too slow when processing many files, so we switched to C++

@click.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False))
def parse(file):
    # drop tsplib xml file type mapping
    ogdf.GraphIO.getFileType("a.xml")
    ogdf.GraphIO.FILE_TYPE_MAP.extract("xml")

    G = ogdf.Graph()
    GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)
    if file.endswith(".gz"):
        import gzip, tempfile, shutil
        with tempfile.NamedTemporaryFile(suffix=file.removesuffix(".gz").split("/")[-1]) as f_out:
            with gzip.open(file, 'rb') as f_in:
                shutil.copyfileobj(f_in, f_out)
            ogdf.GraphIO.read(GA, G, f_out.name)
    else:
        ogdf.GraphIO.read(GA, G, file)

    print("x1;y1;x2;y2")
    for e in G.edges:
        print(";".join(map(str, (GA.x[e.source()], GA.y[e.source()], GA.x[e.target()], GA.y[e.target()]))))


if __name__ == '__main__':
    parse()
