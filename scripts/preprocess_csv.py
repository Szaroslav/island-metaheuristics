import csv
import sys
import os


def remove_duplicate_headers(input_file: str) -> list[list[str]]:
    """
    Reads a CSV file, removes duplicate headers, and returns cleaned rows
    (including header).
    """
    rows: list[list[str]] = []

    with open(input_file, "r", newline="") as infile:
        reader = csv.reader(infile)

        try:
            # First header
            header = next(reader)
        except StopIteration:
            # Empty file
            return []

        rows.append(header)

        for row in reader:
            if row == header:
                continue
            rows.append(row)

    return rows


def merge_csvs(input_dir: str, output_file: str) -> None:
    """
    Merges all CSV files from the input directory into one output file,
    removing duplicate headers from each file and keeping only one global
    header.
    """
    merged_rows: list[list[str]] = []
    header_written: bool = False

    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith(".csv"):
            input_path = os.path.join(input_dir, filename)
            rows = remove_duplicate_headers(input_path)

            if not rows:
                continue

            header, *data = rows

            if not header_written:
                merged_rows.append(header)
                header_written = True

            merged_rows.extend(data)

            print(f"Processed {filename}")

    if merged_rows:
        with open(output_file, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(merged_rows)
        print(f"Merged CSV written to {output_file}")
    else:
        print("No CSV files found or all were empty.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess_csv.py <input_directory> <output_file>")
        sys.exit(1)

    input_dir: str = sys.argv[1]
    output_file: str = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory")
        sys.exit(1)

    merge_csvs(input_dir, output_file)
