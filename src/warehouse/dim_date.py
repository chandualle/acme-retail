import json
from pathlib import Path
from datetime import date, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


def write_json(filename, rows):
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = ANALYTICS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


def build_dim_date(start_date, end_date):
    dimension = []

    current_date = start_date
    date_key = 1

    while current_date <= end_date:

        dimension.append({
            "date_key": date_key,
            "full_date": current_date.isoformat(),
            "year": current_date.year,
            "quarter": ((current_date.month - 1) // 3) + 1,
            "month": current_date.month,
            "month_name": current_date.strftime("%B"),
            "week": current_date.isocalendar().week,
            "day": current_date.day,
            "day_of_week": current_date.isoweekday(),
            "day_name": current_date.strftime("%A"),
            "is_weekend": current_date.isoweekday() >= 6
        })

        current_date += timedelta(days=1)
        date_key += 1

    return dimension


def main():

    print("Starting dim_date build...")
    print()

    # Our generated retail data is in October 2026.
    start_date = date(2026, 1, 1)
    end_date = date(2026, 12, 31)

    dim_date = build_dim_date(
        start_date,
        end_date
    )

    write_json(
        "dim_date.json",
        dim_date
    )

    print(f"Start date:          {start_date}")
    print(f"End date:            {end_date}")
    print(f"Date dimension rows: {len(dim_date)}")

    print()
    print("DIM DATE BUILD COMPLETED")


if __name__ == "__main__":
    main()