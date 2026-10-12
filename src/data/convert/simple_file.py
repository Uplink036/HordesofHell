import csv
from pathlib import Path

INPUT_FILE = (
    Path(__file__).parent.parent / "D4 Infernal Compass - Runs (Season 10).csv"
)
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_FILE_NAME = "simple_output.csv"
OUTPUT_HEADERS = ["Difficulty", "RunID", "RoundID", "Choice", "Total Aether"]


def convert_file_to_simple_format(
    input_file: Path, allow_existing: bool = False
):

    print(f"Converting file: {input_file}")
    with open(input_file, mode="r", newline="") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    if not allow_existing and (OUTPUT_DIR / OUTPUT_FILE_NAME).exists():
        raise FileExistsError(f"The file '{OUTPUT_FILE_NAME}' already exists.")

    print(f"Writing to output file: {OUTPUT_DIR / OUTPUT_FILE_NAME}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / OUTPUT_FILE_NAME, mode="w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=OUTPUT_HEADERS)
        writer.writeheader()
        for row in rows:
            output_row = {}
            for header in OUTPUT_HEADERS:
                value = row.get(header, "")
                if value == "":
                    raise ValueError(
                        f"Missing value for required field '{header}' in row: {row}"
                    )
                else:
                    output_row[header] = value

            writer.writerow(output_row)
    print(f"Finished writing to output file: {OUTPUT_FILE_NAME}")


if __name__ == "__main__":
    convert_file_to_simple_format(INPUT_FILE)
