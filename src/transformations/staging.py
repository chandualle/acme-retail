import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACCEPTED_DIR = PROJECT_ROOT / "data" / "accepted"
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def read_json(filename):
    file_path = ACCEPTED_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, rows):
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    output_file = STAGING_DIR / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


def transform_orders(orders):

    staging_orders = []

    for order in orders:

        quantity = int(order["quantity"])
        unit_price = float(order["unit_price"])
        discount = float(order["discount"])

        total_amount = (
            quantity * unit_price
        ) - discount

        transformed_order = {
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product_id": order["product_id"],
            "store_id": order["store_id"],
            "order_timestamp": order["order_timestamp"],
            "order_date": order["order_timestamp"][:10],
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "total_amount": total_amount,
            "order_status": order["order_status"].upper(),
            "channel": order["channel"].upper(),
            "updated_at": order["updated_at"],
            "staging_timestamp": datetime.now().isoformat()
        }

        staging_orders.append(transformed_order)

    return staging_orders


def main():

    print("Starting staging transformation...")
    print()

    orders = read_json("orders_valid.json")

    staging_orders = transform_orders(orders)

    write_json(
        "orders.json",
        staging_orders
    )

    print(f"Input orders:    {len(orders)}")
    print(f"Staging orders:  {len(staging_orders)}")
    print()
    print("STAGING TRANSFORMATION COMPLETED")


if __name__ == "__main__":
    main()