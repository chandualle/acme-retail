import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"


def main():

    print("Starting analytics queries...")
    print()

    connection = duckdb.connect()

    fact_orders = ANALYTICS_DIR / "fact_orders.json"
    dim_product = ANALYTICS_DIR / "dim_product.json"
    dim_store = ANALYTICS_DIR / "dim_store.json"

    connection.execute(f"""
        CREATE OR REPLACE VIEW fact_orders AS
        SELECT *
        FROM read_json_auto('{fact_orders}')
    """)

    connection.execute(f"""
        CREATE OR REPLACE VIEW dim_product AS
        SELECT *
        FROM read_json_auto('{dim_product}')
    """)

    connection.execute(f"""
        CREATE OR REPLACE VIEW dim_store AS
        SELECT *
        FROM read_json_auto('{dim_store}')
    """)

    print("Warehouse tables loaded.")
    print()

    print("DAILY REVENUE")
    print("------------------------------")

    result = connection.execute("""
        SELECT
            order_date,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM fact_orders
        WHERE order_status = 'COMPLETED'
        GROUP BY order_date
        ORDER BY order_date
    """).fetchall()

    for row in result:
        print(row)

    print()
    print("Analytics query completed.")

    print()
    print("TOP 5 PRODUCTS BY REVENUE")
    print("------------------------------")

    result = connection.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            ROUND(SUM(f.total_amount), 2) AS revenue
        FROM fact_orders f
        INNER JOIN dim_product p
            ON f.product_key = p.product_key
        WHERE f.order_status = 'COMPLETED'
        GROUP BY
            p.product_id,
            p.product_name,
            p.category
        ORDER BY revenue DESC
        LIMIT 5
    """).fetchall()

    for row in result:
        print(row)

    connection.close()


if __name__ == "__main__":
    main()