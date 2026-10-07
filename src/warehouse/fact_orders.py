import json
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_DIR = PROJECT_ROOT / "data" / "staging"
ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


# ============================================================
# READ JSON
# ============================================================

def read_json(directory, filename):

    file_path = directory / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# WRITE JSON
# ============================================================

def write_json(filename, rows):

    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = ANALYTICS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


# ============================================================
# BUILD LOOKUP DICTIONARIES
# ============================================================

def build_customer_lookup(customers):

    lookup = {}

    for customer in customers:
        lookup[customer["customer_id"]] = customer["customer_key"]

    return lookup


def build_product_lookup(products):

    lookup = {}

    for product in products:
        lookup[product["product_id"]] = product["product_key"]

    return lookup


def build_store_lookup(stores):

    lookup = {}

    for store in stores:
        lookup[store["store_id"]] = store["store_key"]

    return lookup


# ============================================================
# BUILD FACT ORDERS
# ============================================================

def build_fact_orders(
    orders,
    customer_lookup,
    product_lookup,
    store_lookup
):

    fact_orders = []
    rejected_orders = []

    for order in orders:

        customer_id = order["customer_id"]
        product_id = order["product_id"]
        store_id = order["store_id"]

        # -----------------------------------------
        # Check customer
        # -----------------------------------------

        if customer_id not in customer_lookup:

            rejected_orders.append({
                "order_id": order["order_id"],
                "reason": "Customer key not found",
                "customer_id": customer_id
            })

            continue

        # -----------------------------------------
        # Check product
        # -----------------------------------------

        if product_id not in product_lookup:

            rejected_orders.append({
                "order_id": order["order_id"],
                "reason": "Product key not found",
                "product_id": product_id
            })

            continue

        # -----------------------------------------
        # Check store
        # -----------------------------------------

        if store_id not in store_lookup:

            rejected_orders.append({
                "order_id": order["order_id"],
                "reason": "Store key not found",
                "store_id": store_id
            })

            continue

        # -----------------------------------------
        # Build fact record
        # -----------------------------------------

        fact_order = {
            "order_id": order["order_id"],

            "customer_key": customer_lookup[customer_id],
            "product_key": product_lookup[product_id],
            "store_key": store_lookup[store_id],

            "order_date": order["order_date"],
            "order_timestamp": order["order_timestamp"],

            "quantity": int(order["quantity"]),
            "unit_price": float(order["unit_price"]),
            "discount": float(order["discount"]),
            "total_amount": float(order["total_amount"]),

            "order_status": order["order_status"],
            "channel": order["channel"],

            "updated_at": order["updated_at"],
            "staging_timestamp": order["staging_timestamp"]
        }

        fact_orders.append(fact_order)

    return fact_orders, rejected_orders


# ============================================================
# MAIN
# ============================================================

def main():

    print("Starting fact_orders build...")
    print()

    # -----------------------------------------
    # Read staging orders
    # -----------------------------------------

    orders = read_json(
        STAGING_DIR,
        "orders.json"
    )

    print(f"Staging orders: {len(orders)}")

    # -----------------------------------------
    # Read dimensions
    # -----------------------------------------

    customers = read_json(
        ANALYTICS_DIR,
        "dim_customer.json"
    )

    products = read_json(
        ANALYTICS_DIR,
        "dim_product.json"
    )

    stores = read_json(
        ANALYTICS_DIR,
        "dim_store.json"
    )

    print(f"Customer dimension: {len(customers)}")
    print(f"Product dimension:  {len(products)}")
    print(f"Store dimension:    {len(stores)}")

    # -----------------------------------------
    # Build lookups
    # -----------------------------------------

    customer_lookup = build_customer_lookup(customers)
    product_lookup = build_product_lookup(products)
    store_lookup = build_store_lookup(stores)

    # -----------------------------------------
    # Build fact table
    # -----------------------------------------

    fact_orders, rejected_orders = build_fact_orders(
        orders,
        customer_lookup,
        product_lookup,
        store_lookup
    )

    # -----------------------------------------
    # Write fact table
    # -----------------------------------------

    write_json(
        "fact_orders.json",
        fact_orders
    )

    print()
    print(f"Fact orders created: {len(fact_orders)}")
    print(f"Rejected orders:     {len(rejected_orders)}")

    # -----------------------------------------
    # Write rejected orders if any
    # -----------------------------------------

    if rejected_orders:

        write_json(
            "fact_orders_rejected.json",
            rejected_orders
        )

        print("Rejected orders written to:")
        print("data/analytics/fact_orders_rejected.json")

    print()
    print("FACT ORDERS BUILD COMPLETED")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()