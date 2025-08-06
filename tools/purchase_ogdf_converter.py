import re
import sys

from ogdf_python import *

## drop tsplib xml file type mapping
# ogdf.GraphIO.getFileType("a.xml")
# ogdf.GraphIO.FILE_TYPE_MAP.extract("xml")

# create storage for the graph and its layout
G = ogdf.Graph()
GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)

## load the graph from an optionally compressed file
file = sys.argv[1]
# if file.endswith(".gz"):
#     import gzip, tempfile, shutil
#
#     with tempfile.NamedTemporaryFile(suffix=file.removesuffix(".gz").split("/")[-1]) as f_out:
#         with gzip.open(file, 'rb') as f_in:
#             shutil.copyfileobj(f_in, f_out)
#         ogdf.GraphIO.read(GA, G, f_out.name)
# else:
#     ogdf.GraphIO.read(GA, G, file)


with open(file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Regex for node and edge lines
node_re = re.compile(r'^(\d+)\s+\{\$.*?NP\s+(\d+)\s+(\d+).*?\$\}"([^"]+)"')
edge_re = re.compile(r'^\s*(\d+)\s+\{\$.*?EL\s+((?:\d+\s+)+)\$\}"')

current_node = None
nodes = {}
edge_lines = []
for line in lines:
    line = line.strip()
    if not line or line == ";" or line == "END":
        current_node = None
        continue
    node_match = node_re.match(line)
    if node_match:
        # Extract node id, position, and label
        node_id = int(node_match.group(1))
        nodes[node_id] = current_node = G.newNode()
        GA.label[current_node] = node_match.group(4).replace("\\n", "\n")
        GA.x[current_node] = float(node_match.group(2))
        GA.y[current_node] = float(node_match.group(3))
        GA.shape[current_node] = ogdf.Shape.Ellipse
        continue
    edge_lines.append((current_node, line))

for (current_node, line) in edge_lines:
    edge_match = edge_re.match(line)
    if edge_match and current_node is not None:
        # Extract edge target and all EL points
        target_id = int(edge_match.group(1))
        target = nodes[target_id]
        edge = G.newEdge(current_node, target)
        GA.arrowType[edge] = getattr(ogdf.EdgeArrow, "None")
        coords = list(map(int, edge_match.group(2).split()))
        # Only use intermediate points as bends (exclude first and last)
        if len(coords) > 4:
            for i in range(2, len(coords) - 2, 2):
                GA.bends[edge].emplaceBack(coords[i], coords[i + 1])

# normalize the drawing
GA.directed = False
GA.translateToNonNeg()
bb = GA.boundingBox()
GA.scale(1024 / (bb.width() or 1024), scaleNodes=False)
GA.setAllWidth(20)
GA.setAllHeight(20)

# targets
s, t = G.nodes[0], G.nodes[1]
GA.fillColor[s] = ogdf.Color.Name.Black
GA.fillColor[t] = ogdf.Color.Name.Black

# and write it out
ogdf.GraphIO.write(GA, file + ".svg")
