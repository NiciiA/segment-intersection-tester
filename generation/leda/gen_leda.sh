#! /bin/bash

if ! [ -e "testsets" ]; then
    mkdir testsets
fi

if ! [ -e "testsets-binary" ]; then
    mkdir testsets-binary
fi

if ! [ -f "gen_leda_sweep_time_random" ]; then
    echo "Please compile gen_leda_sweep_time_random first."
fi

if ! [ -f "gen_leda_sweep_time_difficult" ]; then
    echo "Please compile gen_leda_sweep_time_difficult first."
fi

if ! [ -f "../number_converter.py" ]; then
    echo "Missing number converter in parent directory."
fi

for d in {1..10}; do

    # Generate data sets in the same way as in the LEDA 7.2 Guide, page 121. 

    # Generate "Random" test set
    for ((k=10; k<=60; k+=10)); do # Originally <=100 but this would yield numbers with more than 64 bits.
	./gen_leda_sweep_time_random 200 $k integer > testsets/leda_sweep_time_random_d${d}_k${k}_integer.csv
	python3 ../number_converter.py --file testsets/leda_sweep_time_random_d${d}_k${k}_integer.csv --output testsets-binary/leda_sweep_time_random_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_random 200 $k double > testsets/leda_sweep_time_random_d${d}_k${k}_double.csv
	python3 ../number_converter.py --file testsets/leda_sweep_time_random_d${d}_k${k}_double.csv --output testsets-binary/leda_sweep_time_random_d${d}_k${k}_double.csv
    done 

    # Generate "Difficult" test set
    for ((k=10; k<=60; k+=10)); do # Originally <=100 but this would yield numbers with more than 64 bits.
	./gen_leda_sweep_time_difficult 200 $k 10 integer > testsets/leda_sweep_time_difficult_d${d}_k${k}_integer.csv
	python3 ../number_converter.py --file testsets/leda_sweep_time_difficult_d${d}_k${k}_integer.csv --output testsets-binary/leda_sweep_time_difficult_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_difficult 200 $k 10 double > testsets/leda_sweep_time_difficult_d${d}_k${k}_double.csv
	python3 ../number_converter.py --file testsets/leda_sweep_time_difficult_d${d}_k${k}_double.csv --output testsets-binary/leda_sweep_time_difficult_d${d}_k${k}_double.csv
    done

    # Generate "Highly Degenerate" test set
    # Not needed: ../generator.py is already called with the corresponding arguments.
    # python3 gen_leda_highly_degenerate.py > testsets/leda_highly_degenerate_d${d}.csv

    # Generate shifted-n-gon test set
    for ((N=10; N<=10000; N*=100)); do
	for ((r=800; r<=8000000; r*=100)); do
	    ./gen_leda_circle_segments $N $r > testsets/leda_circle_segments_N${N}_r${r}.csv
	    python3 ../number_converter.py --file testsets/leda_circle_segments_N${N}_r${r}.csv --output testsets-binary/leda_circle_segments_N${N}_r${r}.csv
	done
    done

done
