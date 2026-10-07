import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_DIR = PROJECT_ROOT / "data" / "staging"
ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


def read_json(directory, filename):
    file_path = directory / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, rows):
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = ANALYTICS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


def build_order_lookup(orders):
    lookup = {}

    for order in orders:
        lookup[order["order_id"]] = order

    return lookup


def build_fact_payments(payments, order_lookup):
    fact_payments = []
    rejected_payments = []

    for payment in payments:

        order_id = payment["order_id"]

        # Make sure the payment belongs to a known order
        if order_id not in order_lookup:
            rejected_payments.append({
                "payment_id": payment["payment_id"],
                "order_id": order_id,
                "reason": "Order not found"
            })

            continue

        order = order_lookup[order_id]

        fact_payment = {
            "payment_id": payment["payment_id"],
            "order_id": order_id,

            "customer_key": order["customer_key"],
            "product_key": order["product_key"],
            "store_key": order["store_key"],

            "payment_method": payment["payment_method"],
            "payment_status": payment["payment_status"],
            "amount": float(payment["amount"]),

            "payment_timestamp": payment["payment_timestamp"],
            "updated_at": payment["updated_at"],
            "staging_timestamp": payment["staging_timestamp"]
        }

        fact_payments.append(fact_payment)

    return fact_payments, rejected_payments


def main():

    print("Starting fact_payments build...")
    print()

    payments = read_json(
        STAGING_DIR,
        "payments.json"
    )

    orders = read_json(
        ANALYTICS_DIR,
        "fact_orders.json"
    )

    print(f"Staging payments: {len(payments)}")
    print(f"Fact orders:      {len(orders)}")

    order_lookup = build_order_lookup(orders)

    fact_payments, rejected_payments = build_fact_payments(
        payments,
        order_lookup
    )

    write_json(
        "fact_payments.json",
        fact_payments
    )

    print()
    print(f"Fact payments created: {len(fact_payments)}")
    print(f"Rejected payments:     {len(rejected_payments)}")

    if rejected_payments:

        write_json(
            "fact_payments_rejected.json",
            rejected_payments
        )

        print(
            "Rejected payments written to:"
        )

        print(
            "data/analytics/fact_payments_rejected.json"
        )

    print()
    print("FACT PAYMENTS BUILD COMPLETED")


if __name__ == "__main__":
    main()