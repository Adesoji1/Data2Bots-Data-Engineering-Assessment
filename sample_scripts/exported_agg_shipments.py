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
        FROM adesalu8398_staging.shipments_deliveries AS sd
        JOIN adesalu8398_staging.orders AS o ON sd.order_id = o.order_id
        WHERE sd.shipment_date >= o.order_date + INTERVAL '6 days'
        AND sd.delivery_date IS NULL
    """)

    # Fetch the result
    tt_late_shipments = cur.fetchone()[0]

    # Execute the SQL query to calculate the total number of undelivered shipments
    cur.execute("""
        SELECT COUNT(*) AS tt_undelivered_items
        FROM adesalu8398_staging.shipments_deliveries AS sd
        JOIN adesalu8398_staging.orders AS o ON sd.order_id = o.order_id
        WHERE sd.delivery_date IS NULL
        AND sd.shipment_date IS NULL
        AND '2022-09-05'::date - o.order_date >= 15
    """)

    # Fetch the result
    tt_undelivered_items = cur.fetchone()[0]

    # Insert the results into the agg_shipments table
    cur.execute("""
        INSERT INTO adesalu8398_analytics.agg_shipments (ingestion_date, tt_late_shipments, tt_undelivered_items)
        VALUES ('2022-09-05', %s, %s)
    """, (tt_late_shipments, tt_undelivered_items))

    print("Inserted the results into the agg_shipments table.")

    # Commit the changes
    conn.commit()

    # Write the results to a CSV file
    with open('agg_shipments.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ingestion_date', 'tt_late_shipments', 'tt_undelivered_items'])  # write the header
        writer.writerow(['2022-09-05', tt_late_shipments, tt_undelivered_items])  # write the data

    print("Saved the results to agg_shipments.csv.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and the connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Closed the connection to the database.")
