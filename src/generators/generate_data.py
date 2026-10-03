import csv
import json
from pathlib import Path
from datetime import datetime, date
import random


# --------------------------------------------------
# Configuration
# --------------------------------------------------

OUTPUT_DIR = Path("data/generated")

NUM_CUSTOMERS = 10
NUM_PRODUCTS = 5
NUM_STORES = 3
NUM_ORDERS = 20


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def generate_timestamp():
    return datetime.now().isoformat(timespec="seconds")


# --------------------------------------------------
# Generate customers
# --------------------------------------------------

def generate_customers():
    customers = []

    first_names = [
        "Ravi",
        "Arjun",
        "Priya",
        "Sneha",
        "Rahul",
        "Ananya",
        "Vikram",
        "Neha",
        "Kiran",
        "Pooja"
    ]

    last_names = [
        "Kumar",
        "Reddy",
        "Sharma",
        "Patel",
        "Singh"
    ]

    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            "customer_id": f"C{i:04d}",
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "email": f"customer{i}@example.com",
            "phone": f"98{random.randint(10000000, 99999999)}",
            "city": "Vijayawada",
            "state": "AP",
            "country": "India",
            "signup_date": "2026-01-01",
            "customer_status": "ACTIVE",
            "updated_at": generate_timestamp()
        })

    return customers


# --------------------------------------------------
# Generate products
# --------------------------------------------------

def generate_products():
    products = []

    product_names = [
        ("Wireless Mouse", "Electronics"),
        ("Keyboard", "Electronics"),
        ("USB Cable", "Accessories"),
        ("Headphones", "Electronics"),
        ("Laptop Bag", "Accessories")
    ]

    for i in range(1, NUM_PRODUCTS + 1):
        name, category = product_names[i - 1]

        products.append({
            "product_id": f"P{i:04d}",
            "product_name": name,
            "category": category,
            "subcategory": "General",
            "brand": "Acme",
            "supplier_id": f"SUP{i:03d}",
            "unit_cost": random.randint(300, 1500),
            "selling_price": random.randint(800, 2500),
            "product_status": "ACTIVE",
            "updated_at": generate_timestamp()
        })

    return products


# --------------------------------------------------
# Generate stores
# --------------------------------------------------

def generate_stores():
    stores = []

    cities = [
        "Vijayawada",
        "Guntur",
        "Visakhapatnam"
    ]

    for i in range(1, NUM_STORES + 1):
        stores.append({
            "store_id": f"S{i:03d}",
            "store_name": f"Acme Store {i}",
            "city": cities[i - 1],
            "state": "AP",
            "region": "South",
            "store_type": "RETAIL",
            "opening_date": "2024-01-01",
            "store_status": "ACTIVE",
            "updated_at": generate_timestamp()
        })

    return stores


# --------------------------------------------------
# Write CSV
# --------------------------------------------------

def write_csv(filename, rows):
    if not rows:
        return

    output_file = OUTPUT_DIR / filename

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {output_file}")


# --------------------------------------------------
# Write JSON
# --------------------------------------------------

def write_json(filename, rows):
    output_file = OUTPUT_DIR / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    print(f"Created {output_file}")

def read_csv(filename):
    input_file = OUTPUT_DIR / filename

    with open(input_file, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

# --------------------------------------------------
# Orders
# --------------------------------------------------

def generate_orders(customers, products, stores):
    orders = []

    order_statuses = [
        "COMPLETED",
        "COMPLETED",
        "COMPLETED",
        "CANCELLED"
    ]

    channels = [
        "ONLINE",
        "STORE",
        "MOBILE_APP"
    ]

    for i in range(1, NUM_ORDERS + 1):

        customer = random.choice(customers)
        product = random.choice(products)
        store = random.choice(stores)

        quantity = random.randint(1, 5)

        unit_price = float(product["selling_price"])

        discount = random.choice([
            0,
            0,
            0,
            50,
            100
        ])

        order = {
            "order_id": f"O{i:06d}",
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "store_id": store["store_id"],
            "order_timestamp": generate_timestamp(),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "order_status": random.choice(order_statuses),
            "channel": random.choice(channels),
            "updated_at": generate_timestamp()
        }

        orders.append(order)

    return orders

# --------------------------------------------------
# Payments
# --------------------------------------------------

def generate_payments(orders):
    payments = []

    payment_methods = [
        "UPI",
        "CREDIT_CARD",
        "DEBIT_CARD",
        "NET_BANKING",
        "WALLET"
    ]

    for i, order in enumerate(orders, start=1):

        total_amount = (
            order["quantity"] * order["unit_price"]
        ) - order["discount"]

        if order["order_status"] == "COMPLETED":
            payment_status = "SUCCESS"
        else:
            payment_status = "FAILED"

        payment = {
            "payment_id": f"PAY{i:06d}",
            "order_id": order["order_id"],
            "payment_method": random.choice(payment_methods),
            "payment_status": payment_status,
            "amount": total_amount,
            "payment_timestamp": generate_timestamp(),
            "updated_at": generate_timestamp()
        }

        payments.append(payment)

    return payments

# --------------------------------------------------
# Inventory
# --------------------------------------------------

def generate_inventory(products, stores):
    inventory = []

    inventory_id = 1

    for store in stores:
        for product in products:

            stock_quantity = random.randint(0, 100)
            reorder_level = random.randint(10, 30)

            inventory.append({
                "inventory_id": f"INV{inventory_id:06d}",
                "store_id": store["store_id"],
                "product_id": product["product_id"],
                "stock_quantity": stock_quantity,
                "reorder_level": reorder_level,
                "updated_at": generate_timestamp()
            })

            inventory_id += 1

    return inventory

# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Master data
    customers = generate_customers()
    products = generate_products()
    stores = generate_stores()

    write_csv("customers.csv", customers)
    write_csv("products.csv", products)
    write_csv("stores.csv", stores)

    # Transaction data
    orders = generate_orders(
        customers,
        products,
        stores
    )

    write_json("orders.json", orders)

    # Payment data
    payments = generate_payments(orders)

    write_json("payments.json", payments)

    # Inventory data
    inventory = generate_inventory(
        products,
        stores
    )

    write_csv("inventory.csv", inventory)

    print()
    print("Data generation completed.")

if __name__ == "__main__":
    main()