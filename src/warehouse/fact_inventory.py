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


def build_fact_inventory(
    inventory,
    product_lookup,
    store_lookup
):
    fact_inventory = []
    rejected_inventory = []

    for item in inventory:

        product_id = item["product_id"]
        store_id = item["store_id"]

        # Validate product relationship
        if product_id not in product_lookup:
            rejected_inventory.append({
                "inventory_id": item["inventory_id"],
                "product_id": product_id,
                "store_id": store_id,
                "reason": "Product not found"
            })

            continue

        # Validate store relationship
        if store_id not in store_lookup:
            rejected_inventory.append({
                "inventory_id": item["inventory_id"],
                "product_id": product_id,
                "store_id": store_id,
                "reason": "Store not found"
            })

            continue

        stock_quantity = int(item["stock_quantity"])
        reorder_level = int(item["reorder_level"])

        fact_item = {
            "inventory_id": item["inventory_id"],

            "product_key": product_lookup[product_id],
            "store_key": store_lookup[store_id],

            "stock_quantity": stock_quantity,
            "reorder_level": reorder_level,

            "low_inventory_flag": stock_quantity < reorder_level,

            "updated_at": item["updated_at"],
            "staging_timestamp": item["staging_timestamp"]
        }

        fact_inventory.append(fact_item)

    return fact_inventory, rejected_inventory


def main():

    print("Starting fact_inventory build...")
    print()

    inventory = read_json(
        STAGING_DIR,
        "inventory.json"
    )

    products = read_json(
        ANALYTICS_DIR,
        "dim_product.json"
    )

    stores = read_json(
        ANALYTICS_DIR,
        "dim_store.json"
    )

    print(f"Staging inventory: {len(inventory)}")
    print(f"Product dimension: {len(products)}")
    print(f"Store dimension:   {len(stores)}")

    product_lookup = build_product_lookup(products)
    store_lookup = build_store_lookup(stores)

    fact_inventory, rejected_inventory = build_fact_inventory(
        inventory,
        product_lookup,
        store_lookup
    )

    write_json(
        "fact_inventory.json",
        fact_inventory
    )

    print()
    print(f"Fact inventory created: {len(fact_inventory)}")
    print(f"Rejected inventory:     {len(rejected_inventory)}")

    if rejected_inventory:

        write_json(
            "fact_inventory_rejected.json",
            rejected_inventory
        )

        print(
            "Rejected inventory written to:"
        )

        print(
            "data/analytics/fact_inventory_rejected.json"
        )

    print()
    print("FACT INVENTORY BUILD COMPLETED")


if __name__ == "__main__":
    main()