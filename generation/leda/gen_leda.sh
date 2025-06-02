#! /bin/bash

if ! [ -e "testsets" ]; then
    mkdir testsets
fi

if ! [ -f "gen_leda_sweep_time_random" ]; then
    echo "Please compile gen_leda_sweep_time_random first."
fi

if ! [ -f "gen_leda_sweep_time_difficult" ]; then
    echo "Please compile gen_leda_sweep_time_difficult first."
fi

# Generate 10 data sets in the same way as in the LEDA 7.2 Guide, page 121.
for d in {1..10}; do

    # Generate "Random" test set
    for ((k=10; k<=100; k+=10)); do
	./gen_leda_sweep_time_random 200 $k integer > testsets/leda_sweep_time_random_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_random 200 $k double > testsets/leda_sweep_time_random_d${d}_k${k}_double.csv
    done

    # Generate "Difficult" test set
    for ((k=10; k<=100; k+=10)); do
	./gen_leda_sweep_time_difficult 200 $k 10 integer > testsets/leda_sweep_time_difficult_d${d}_k${k}_integer.csv
	./gen_leda_sweep_time_difficult 200 $k 10 double > testsets/leda_sweep_time_difficult_d${d}_k${k}_double.csv
    done
done

