import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"


def convert_json_to_jsonl(input_filename, output_filename):

    input_file = GENERATED_DIR / input_filename
    output_file = GENERATED_DIR / output_filename

    with open(input_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    print(f"Converted: {input_filename}")
    print(f"Created:   {output_filename}")
    print(f"Records:   {len(records)}")
    print()


def main():

    convert_json_to_jsonl(
        "orders.json",
        "orders.jsonl"
    )

    convert_json_to_jsonl(
        "payments.json",
        "payments.jsonl"
    )


if __name__ == "__main__":
    main()