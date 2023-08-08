import psycopg2
import csv

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="d2b_accessment",
        user="adesalu8398",
        password="c7CPYwmPGm",
        host="34.89.230.185",
        port="5432"
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("Connected to the database.")

    # Execute the SQL query to calculate the total number of late shipments
    cur.execute("""
        SELECT COUNT(*) AS tt_late_shipments
        FROM adesalu8398_staging.shipments_deliveries
        WHERE shipment_date >= order_date + INTERVAL '6 days'
        AND delivery_date IS NULL
    """)

    # Fetch the result and save it to a CSV file
    with open('late_shipments.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tt_late_shipments'])  # write the header
        writer.writerow(cur.fetchone())  # write the data

    print("Saved the result to late_shipments.csv.")

    # Execute the SQL query to calculate the total number of undelivered shipments
    cur.execute("""
        SELECT COUNT(*) AS tt_undelivered_items
        FROM adesalu8398_staging.shipments_deliveries
        WHERE delivery_date IS NULL
        AND shipment_date IS NULL
        AND '2022-09-05'::date - order_date >= 15
    """)

    # Fetch the result and save it to a CSV file
    with open('undelivered_shipments.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tt_undelivered_items'])  # write the header
        writer.writerow(cur.fetchone())  # write the data

    print("Saved the result to undelivered_shipments.csv.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and the connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Closed the connection to the database.")
