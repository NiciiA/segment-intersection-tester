from generator import random_int, save_segments_to_csv


def main():
    num_calls = 100
    num_segments = 100
    max_coord = 10

    for i in range(num_calls):
        segments = random_int(num_segments, max_coord)
        filename = f"random_segments_{i + 1}.csv"
        save_segments_to_csv(segments, filename)

    print(f"Saved {num_calls} CSV files in 'tests/' directory")


if __name__ == "__main__":
    main()
