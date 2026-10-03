import csv
import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "generated"
ACCEPTED_DIR = PROJECT_ROOT / "data" / "accepted"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine"


def read_csv(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_csv(filename, rows, output_dir):
    if not rows:
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


def write_json(filename, rows, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


def validate_orders(orders, customers, products, stores):

    valid_customer_ids = {
        row["customer_id"]
        for row in customers
    }

    valid_product_ids = {
        row["product_id"]
        for row in products
    }

    valid_store_ids = {
        row["store_id"]
        for row in stores
    }

    valid_orders = []
    invalid_orders = []

    seen_order_ids = set()

    for order in orders:

        errors = []

        order_id = order.get("order_id")

        # Duplicate order
        if order_id in seen_order_ids:
            errors.append("DUPLICATE_ORDER_ID")

        seen_order_ids.add(order_id)

        # Customer validation
        customer_id = order.get("customer_id")

        if not customer_id:
            errors.append("MISSING_CUSTOMER_ID")

        elif customer_id not in valid_customer_ids:
            errors.append("UNKNOWN_CUSTOMER_ID")

        # Product validation
        product_id = order.get("product_id")

        if product_id not in valid_product_ids:
            errors.append("UNKNOWN_PRODUCT_ID")

        # Store validation
        store_id = order.get("store_id")

        if store_id not in valid_store_ids:
            errors.append("UNKNOWN_STORE_ID")

        # Quantity validation
        try:
            quantity = int(order["quantity"])

            if quantity <= 0:
                errors.append("INVALID_QUANTITY")

        except (ValueError, TypeError):
            errors.append("INVALID_QUANTITY")

        # Discount validation
        try:
            discount = float(order["discount"])

            if discount < 0:
                errors.append("INVALID_DISCOUNT")

        except (ValueError, TypeError):
            errors.append("INVALID_DISCOUNT")

        # Decide where the record goes
        if errors:

            invalid_orders.append({
                **order,
                "error_type": "|".join(errors),
                "quarantine_timestamp": datetime.now().isoformat()
            })

        else:
            valid_orders.append(order)

    return valid_orders, invalid_orders


def main():

    print("Starting quarantine pipeline...")
    print()

    customers = read_csv("customers.csv")
    products = read_csv("products.csv")
    stores = read_csv("stores.csv")
    orders = read_json("orders.json")

    valid_orders, invalid_orders = validate_orders(
        orders,
        customers,
        products,
        stores
    )

    # Write accepted records
    write_json(
        "orders_valid.json",
        valid_orders,
        ACCEPTED_DIR
    )

    # Write rejected records
    write_json(
        "orders_quarantine.json",
        invalid_orders,
        QUARANTINE_DIR
    )

    print(f"Total orders:       {len(orders)}")
    print(f"Valid orders:       {len(valid_orders)}")
    print(f"Quarantined orders: {len(invalid_orders)}")
    print()

    if invalid_orders:
        print("Some records were quarantined.")
    else:
        print("All records passed validation.")


if __name__ == "__main__":
    main()