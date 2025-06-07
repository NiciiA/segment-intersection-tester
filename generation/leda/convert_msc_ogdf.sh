for inp in msc-graphstudy/data/layouts/**/*.xml.gz; do
    d="$(basename $(dirname $inp))"
    f="$(basename $inp).csv"
    mkdir -p "$d"
    out="$d/$f"

    if [[ -s "$out" ]]; then
        echo "skipping $out"
    else
        echo "processing $out"
        # python segment-intersection/generation/ogdf_converter.py $inp > $out
        segment-intersection/generation/leda/ogdf_to_segint $inp > $out
    fi
done
