#! /bin/bash

TEMP_DIR="testsets"
# TEMP_BINARY_DIR="testsets-binary"
OUTPUT_DIR="../tests/"

if ! [ -e $TEMP_DIR ]; then
    mkdir $TEMP_DIR
fi

# if ! [ -e $TEMP_BINARY_DIR ]; then
#     mkdir $TEMP_BINARY_DIR
# fi

if ! [ -e $OUTPUT_DIR ]; then
    mkdir $OUTPUT_DIR
fi

if ! [ -f "gen_leda_sweep_time_random" ]; then
    echo "Please compile gen_leda_sweep_time_random first."
fi

if ! [ -f "gen_leda_sweep_time_difficult" ]; then
    echo "Please compile gen_leda_sweep_time_difficult first."
fi

if ! [ -f "gen_leda_geo_sweep_intersection_time" ]; then
    echo "Please compile gen_leda_geo_sweep_intersection_time first."
fi

if ! [ -f "../number_converter.py" ]; then
    echo "Missing number converter in parent directory."
fi

for d in {1..10}; do

    # Generate data sets in the same way as in the LEDA 7.2 Guide, page 121. 

    # Generate "Random" test set
    for ((k=10; k<=60; k+=10)); do # Originally <=100 but this would yield numbers with more than 64 bits.
	./gen_leda_sweep_time_random 200 $k integer > ${TEMP_DIR}/leda_sweep_time_random_d${d}_k${k}_integer.csv
	python3 ../number_converter.py --file $TEMP_DIR/leda_sweep_time_random_d${d}_k${k}_integer.csv --output ${OUTPUT_DIR}/leda_sweep_time_random_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_random 200 $k double > ${TEMP_DIR}/leda_sweep_time_random_d${d}_k${k}_double.csv
	python3 ../number_converter.py --file ${TEMP_DIR}/leda_sweep_time_random_d${d}_k${k}_double.csv --output ${OUTPUT_DIR}/leda_sweep_time_random_d${d}_k${k}_double.csv
    done 

    # Generate "Difficult" test set
    for ((k=10; k<=60; k+=10)); do # Originally <=100 but this would yield numbers with more than 64 bits.
	./gen_leda_sweep_time_difficult 200 $k 10 integer > ${TEMP_DIR}/leda_sweep_time_difficult_d${d}_k${k}_integer.csv
	python3 ../number_converter.py --file ${TEMP_DIR}/leda_sweep_time_difficult_d${d}_k${k}_integer.csv --output testsets-binary/leda_sweep_time_difficult_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_difficult 200 $k 10 double > ${TEMP_DIR}/leda_sweep_time_difficult_d${d}_k${k}_double.csv
	python3 ../number_converter.py --file ${TEMP_DIR}/leda_sweep_time_difficult_d${d}_k${k}_double.csv --output ${OUTPUT_DIR}/leda_sweep_time_difficult_d${d}_k${k}_double.csv
    done

    # Generate "Highly Degenerate" test set
    # Not needed: ../generator.py is already called with the corresponding arguments.
    # python3 gen_leda_highly_degenerate.py > testsets/leda_highly_degenerate_d${d}.csv

    # Generate "Sweep Intersection Time" test set as in the LEDA book: each instance with 2000 segments, each with one endpoint being a 30 bits random integer and the other the same integer with an added 5-bit random integer.
    ./gen_leda_geo_sweep_intersection_time 2000 30 5 > ${TEMP_DIR}/leda_geo_sweep_intersection_time_d${d}_N2000_k30_s5.csv
    python3 ../number_converter.py --file ${TEMP_DIR}/leda_geo_sweep_intersection_time_d${d}_N2000_k30_s5.csv --output ${OUTPUT_DIR}/leda_geo_sweep_intersection_time_d${d}_N2000_k30_s5.csv
done

# Generate shifted-n-gon test set
for ((N=10; N<=10000; N*=100)); do
    for ((r=800; r<=8000000; r*=100)); do
	./gen_leda_circle_segments $N $r > testsets/leda_circle_segments_N${N}_r${r}.csv
	python3 ../number_converter.py --file testsets/leda_circle_segments_N${N}_r${r}.csv --output testsets-binary/leda_circle_segments_N${N}_r${r}.csv
    done
done
