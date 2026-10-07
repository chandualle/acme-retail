import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_DIR = PROJECT_ROOT / "data" / "staging"
ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


# ============================================================
# READ / WRITE FUNCTIONS
# ============================================================

def read_json(filename):

    file_path = STAGING_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, rows):

    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = ANALYTICS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


# ============================================================
# DIM CUSTOMER
# ============================================================

def build_dim_customer(customers):

    dimension = []

    for index, customer in enumerate(customers, start=10001):

        dimension.append({
            "customer_key": index,
            "customer_id": customer["customer_id"],
            "first_name": customer["first_name"],
            "last_name": customer["last_name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "city": customer["city"],
            "state": customer["state"],
            "country": customer["country"],
            "signup_date": customer["signup_date"],
            "customer_status": customer["customer_status"],
            "updated_at": customer["updated_at"]
        })

    return dimension


# ============================================================
# DIM PRODUCT
# ============================================================

def build_dim_product(products):

    dimension = []

    for index, product in enumerate(products, start=20001):

        dimension.append({
            "product_key": index,
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "brand": product["brand"],
            "supplier_id": product["supplier_id"],
            "unit_cost": float(product["unit_cost"]),
            "selling_price": float(product["selling_price"]),
            "product_status": product["product_status"],
            "updated_at": product["updated_at"]
        })

    return dimension


# ============================================================
# DIM STORE
# ============================================================

def build_dim_store(stores):

    dimension = []

    for index, store in enumerate(stores, start=30001):

        dimension.append({
            "store_key": index,
            "store_id": store["store_id"],
            "store_name": store["store_name"],
            "city": store["city"],
            "state": store["state"],
            "region": store["region"],
            "store_type": store["store_type"],
            "opening_date": store["opening_date"],
            "store_status": store["store_status"],
            "updated_at": store["updated_at"]
        })

    return dimension


# ============================================================
# MAIN
# ============================================================

def main():

    print("Starting warehouse dimension build...")
    print()

    # -----------------------------------------
    # Customer Dimension
    # -----------------------------------------

    print("Building dim_customer...")

    customers = read_json("customers.json")

    dim_customer = build_dim_customer(customers)

    write_json(
        "dim_customer.json",
        dim_customer
    )

    print(f"Customers read:       {len(customers)}")
    print(f"Dimension records:    {len(dim_customer)}")
    print("dim_customer created successfully.")
    print()

    # -----------------------------------------
    # Product Dimension
    # -----------------------------------------

    print("Building dim_product...")

    products = read_json("products.json")

    dim_product = build_dim_product(products)

    write_json(
        "dim_product.json",
        dim_product
    )

    print(f"Products read:        {len(products)}")
    print(f"Dimension records:    {len(dim_product)}")
    print("dim_product created successfully.")
    print()

    # -----------------------------------------
    # Store Dimension
    # -----------------------------------------

    print("Building dim_store...")

    stores = read_json("stores.json")

    dim_store = build_dim_store(stores)

    write_json(
        "dim_store.json",
        dim_store
    )

    print(f"Stores read:          {len(stores)}")
    print(f"Dimension records:    {len(dim_store)}")
    print("dim_store created successfully.")
    print()

    print("WAREHOUSE DIMENSIONS COMPLETED")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()