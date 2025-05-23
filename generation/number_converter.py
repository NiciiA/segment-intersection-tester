import argparse
import pandas as pd
import struct


def float2bin(number, hexdecimal=False, single=False):
    bytes_data = struct.pack('>f' if single else '>d', number)
    func, length = (hex, 2) if hexdecimal else (bin, 8)
    byte2bin = lambda byte: func(byte)[2:].rjust(length, '0')
    return ''.join(map(byte2bin, bytes_data))


def convert_csv_to_binary(input_path, output_path):
    # Load input CSV with ';' as delimiter
    df = pd.read_csv(input_path, sep=';')

    # Convert each float to 64-bit binary using float2bin
    binary_df = df.applymap(lambda x: float2bin(float(x)))

    # Save the result
    binary_df.to_csv(output_path, index=False, sep=';')
    print(f"Binary CSV written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert CSV floats to 64-bit IEEE binary strings.")
    parser.add_argument('-f', '--file', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')

    args = parser.parse_args()
    convert_csv_to_binary(args.file, args.output)


if __name__ == "__main__":
    main()
