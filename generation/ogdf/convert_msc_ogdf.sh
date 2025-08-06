# needs to be run in a directory that contains the `msc-graphstudy` and `segment-intersection` repos next to each other

for inp in msc-graphstudy/data/layouts/**/*.xml.gz; do
    d="tests/msc/$(basename $(dirname $inp))"
    mkdir -p "$d"
    out_float="$d/$(basename $inp).csv.tmp"
    out_bin="$d/$(basename $inp).csv"

    if [[ -s "$out" ]]; then
        echo "skipping $out"
    else
        echo "processing $out"
        # python segment-intersection/generation/ogdf/ogdf_converter.py $inp > $out
        segment-intersection/generation/ogdf/ogdf_to_segint $inp > $out_float
        segintbench-convert float2bin $out_float $out_bin
    fi
done
