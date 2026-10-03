import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "generated"


def read_csv(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_required_columns(rows, required_columns, dataset_name):
    errors = []

    if not rows:
        errors.append(f"{dataset_name}: dataset is empty")
        return errors

    actual_columns = set(rows[0].keys())

    for column in required_columns:
        if column not in actual_columns:
            errors.append(
                f"{dataset_name}: missing column '{column}'"
            )

    return errors


def check_unique(rows, column, dataset_name):
    errors = []

    seen = set()

    for row in rows:
        value = row.get(column)

        if value in seen:
            errors.append(
                f"{dataset_name}: duplicate {column}={value}"
            )

        seen.add(value)

    return errors


def check_positive_integer(rows, column, dataset_name):
    errors = []

    for row in rows:
        try:
            value = int(row[column])

            if value <= 0:
                errors.append(
                    f"{dataset_name}: {column} must be > 0, "
                    f"found {value}"
                )

        except (ValueError, TypeError):
            errors.append(
                f"{dataset_name}: invalid integer "
                f"in {column}: {row[column]}"
            )

    return errors


def check_foreign_keys(
    child_rows,
    child_column,
    parent_rows,
    parent_column,
    dataset_name
):
    errors = []

    valid_values = {
        row[parent_column]
        for row in parent_rows
    }

    for row in child_rows:
        value = row.get(child_column)

        if value is None or value == "":
            continue

        if value not in valid_values:
            errors.append(
                f"{dataset_name}: {child_column}={value} "
                f"does not exist in parent dataset"
            )

    return errors


def main():

    errors = []

    print("Starting data quality checks...")
    print()

    # -----------------------------------------
    # Load datasets
    # -----------------------------------------

    customers = read_csv("customers.csv")
    products = read_csv("products.csv")
    stores = read_csv("stores.csv")
    orders = read_json("orders.json")
    payments = read_json("payments.json")
    inventory = read_csv("inventory.csv")

    # -----------------------------------------
    # Required columns
    # -----------------------------------------

    errors += check_required_columns(
        customers,
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "signup_date",
            "customer_status",
            "updated_at"
        ],
        "customers"
    )

    errors += check_required_columns(
        products,
        [
            "product_id",
            "product_name",
            "category",
            "unit_cost",
            "selling_price",
            "product_status",
            "updated_at"
        ],
        "products"
    )

    errors += check_required_columns(
        stores,
        [
            "store_id",
            "store_name",
            "city",
            "state",
            "region",
            "store_type",
            "opening_date",
            "store_status",
            "updated_at"
        ],
        "stores"
    )

    errors += check_required_columns(
        orders,
        [
            "order_id",
            "customer_id",
            "product_id",
            "store_id",
            "order_timestamp",
            "quantity",
            "unit_price",
            "discount",
            "order_status",
            "channel",
            "updated_at"
        ],
        "orders"
    )

    errors += check_required_columns(
        payments,
        [
            "payment_id",
            "order_id",
            "payment_method",
            "payment_status",
            "amount",
            "payment_timestamp",
            "updated_at"
        ],
        "payments"
    )

    errors += check_required_columns(
        inventory,
        [
            "inventory_id",
            "store_id",
            "product_id",
            "stock_quantity",
            "reorder_level",
            "updated_at"
        ],
        "inventory"
    )

    # -----------------------------------------
    # Primary key checks
    # -----------------------------------------

    errors += check_unique(
        customers,
        "customer_id",
        "customers"
    )

    errors += check_unique(
        products,
        "product_id",
        "products"
    )

    errors += check_unique(
        stores,
        "store_id",
        "stores"
    )

    errors += check_unique(
        orders,
        "order_id",
        "orders"
    )

    errors += check_unique(
        payments,
        "payment_id",
        "payments"
    )

    errors += check_unique(
        inventory,
        "inventory_id",
        "inventory"
    )

    # -----------------------------------------
    # Quantity validation
    # -----------------------------------------

    errors += check_positive_integer(
        orders,
        "quantity",
        "orders"
    )

    # -----------------------------------------
    # Foreign key checks
    # -----------------------------------------

    errors += check_foreign_keys(
        orders,
        "customer_id",
        customers,
        "customer_id",
        "orders"
    )

    errors += check_foreign_keys(
        orders,
        "product_id",
        products,
        "product_id",
        "orders"
    )

    errors += check_foreign_keys(
        orders,
        "store_id",
        stores,
        "store_id",
        "orders"
    )

    errors += check_foreign_keys(
        payments,
        "order_id",
        orders,
        "order_id",
        "payments"
    )

    errors += check_foreign_keys(
        inventory,
        "store_id",
        stores,
        "store_id",
        "inventory"
    )

    errors += check_foreign_keys(
        inventory,
        "product_id",
        products,
        "product_id",
        "inventory"
    )

    # -----------------------------------------
    # Result
    # -----------------------------------------

    print(f"Customers: {len(customers)}")
    print(f"Products:  {len(products)}")
    print(f"Stores:    {len(stores)}")
    print(f"Orders:    {len(orders)}")
    print(f"Payments:  {len(payments)}")
    print(f"Inventory: {len(inventory)}")
    print()

    if errors:
        print("DATA QUALITY CHECK FAILED")
        print("=" * 40)

        for error in errors:
            print(f"[ERROR] {error}")

        raise SystemExit(1)

    print("DATA QUALITY CHECK PASSED")


if __name__ == "__main__":
    main()