import json
import csv
from pathlib import Path
from datetime import datetime


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACCEPTED_DIR = PROJECT_ROOT / "data" / "accepted"
GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


# ============================================================
# READ FUNCTIONS
# ============================================================

def read_json(filename):
    file_path = ACCEPTED_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_csv(filename):
    file_path = ACCEPTED_DIR / filename

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))


def read_generated_csv(filename):
    file_path = GENERATED_DIR / filename

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))

def read_generated_json(filename):
    file_path = GENERATED_DIR / filename

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# WRITE FUNCTION
# ============================================================

def write_json(filename, rows):
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    output_file = STAGING_DIR / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


# ============================================================
# ORDERS TRANSFORMATION
# ============================================================

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


# ============================================================
# CUSTOMERS TRANSFORMATION
# ============================================================

def transform_customers(customers):

    latest_customers = {}

    # Keep latest version of each customer
    for customer in customers:

        customer_id = customer["customer_id"]

        if customer_id not in latest_customers:
            latest_customers[customer_id] = customer
            continue

        existing_timestamp = datetime.fromisoformat(
            latest_customers[customer_id]["updated_at"]
        )

        new_timestamp = datetime.fromisoformat(
            customer["updated_at"]
        )

        if new_timestamp > existing_timestamp:
            latest_customers[customer_id] = customer

    staging_customers = []

    for customer in latest_customers.values():

        staging_customers.append({
            "customer_id": customer["customer_id"],
            "first_name": customer["first_name"].strip(),
            "last_name": customer["last_name"].strip(),
            "email": customer["email"].strip().lower(),
            "phone": customer["phone"],
            "city": customer["city"].strip()
                if customer["city"]
                else None,
            "state": customer["state"].strip()
                if customer["state"]
                else None,
            "country": customer["country"].strip()
                if customer["country"]
                else None,
            "signup_date": customer["signup_date"],
            "customer_status": customer["customer_status"].upper(),
            "updated_at": customer["updated_at"]
        })

    return staging_customers


# ============================================================
# PRODUCTS TRANSFORMATION
# ============================================================

def transform_products(products):

    staging_products = []

    for product in products:

        transformed_product = {
            "product_id": product["product_id"].strip(),
            "product_name": product["product_name"].strip(),
            "category": product["category"].strip(),
            "subcategory": product["subcategory"].strip(),
            "brand": product["brand"].strip(),
            "supplier_id": product["supplier_id"].strip(),
            "unit_cost": float(product["unit_cost"]),
            "selling_price": float(product["selling_price"]),
            "product_status": product["product_status"].strip().upper(),
            "updated_at": product["updated_at"].strip()
        }

        staging_products.append(transformed_product)

    return staging_products

# ============================================================
# STORES TRANSFORMATION
# ============================================================

def transform_stores(stores):

    staging_stores = []

    for store in stores:

        transformed_store = {
            "store_id": store["store_id"].strip(),
            "store_name": store["store_name"].strip(),
            "city": store["city"].strip(),
            "state": store["state"].strip(),
            "region": store["region"].strip(),
            "store_type": store["store_type"].strip().upper(),
            "opening_date": store["opening_date"].strip(),
            "store_status": store["store_status"].strip().upper(),
            "updated_at": store["updated_at"].strip()
        }

        staging_stores.append(transformed_store)

    return staging_stores

# ============================================================
# PAYMENTS TRANSFORMATION
# ============================================================

def transform_payments(payments):

    staging_payments = []

    for payment in payments:

        transformed_payment = {
            "payment_id": payment["payment_id"].strip(),
            "order_id": payment["order_id"].strip(),
            "payment_method": payment["payment_method"].strip().upper(),
            "payment_status": payment["payment_status"].strip().upper(),
            "amount": float(payment["amount"]),
            "payment_timestamp": payment["payment_timestamp"].strip(),
            "updated_at": payment["updated_at"].strip(),
            "staging_timestamp": datetime.now().isoformat()
        }

        staging_payments.append(transformed_payment)

    return staging_payments

# ============================================================
# INVENTORY TRANSFORMATION
# ============================================================

def transform_inventory(inventory):

    staging_inventory = []

    for item in inventory:

        transformed_inventory = {
            "inventory_id": item["inventory_id"].strip(),
            "store_id": item["store_id"].strip(),
            "product_id": item["product_id"].strip(),
            "stock_quantity": int(item["stock_quantity"]),
            "reorder_level": int(item["reorder_level"]),
            "updated_at": item["updated_at"].strip(),
            "staging_timestamp": datetime.now().isoformat()
        }

        staging_inventory.append(transformed_inventory)

    return staging_inventory

# ============================================================
# MAIN
# ============================================================

def main():

    print("Starting staging transformation...")
    print()

    # -----------------------------------------
    # Orders
    # -----------------------------------------

    orders = read_json("orders_valid.json")

    staging_orders = transform_orders(orders)

    write_json(
        "orders.json",
        staging_orders
    )

    print(f"Input orders:      {len(orders)}")
    print(f"Staging orders:    {len(staging_orders)}")

    # -----------------------------------------
    # Customers
    # -----------------------------------------

    customers = read_csv("customers_valid.csv")

    staging_customers = transform_customers(customers)

    write_json(
        "customers.json",
        staging_customers
    )

    print(f"Input customers:   {len(customers)}")
    print(f"Staging customers: {len(staging_customers)}")

    # -----------------------------------------
    # Products
    # -----------------------------------------

    products = read_generated_csv("products.csv")

    staging_products = transform_products(products)

    write_json(
        "products.json",
        staging_products
    )

    print(f"Input products:    {len(products)}")
    print(f"Staging products:  {len(staging_products)}")

    # -----------------------------------------
    # Stores
    # -----------------------------------------

    stores = read_generated_csv("stores.csv")

    staging_stores = transform_stores(stores)

    write_json(
        "stores.json",
        staging_stores
    )

    print(f"Input stores:      {len(stores)}")
    print(f"Staging stores:    {len(staging_stores)}")

    # -----------------------------------------
    # Payments
    # -----------------------------------------

    payments = read_generated_json("payments.json")

    staging_payments = transform_payments(payments)

    write_json(
        "payments.json",
        staging_payments
    )

    print(f"Input payments:    {len(payments)}")
    print(f"Staging payments:  {len(staging_payments)}")

    # -----------------------------------------
    # Inventory
    # -----------------------------------------

    inventory = read_generated_csv("inventory.csv")

    staging_inventory = transform_inventory(inventory)

    write_json(
        "inventory.json",
        staging_inventory
    )

    print(f"Input inventory:   {len(inventory)}")
    print(f"Staging inventory: {len(staging_inventory)}")

    print()
    print("STAGING TRANSFORMATION COMPLETED")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()