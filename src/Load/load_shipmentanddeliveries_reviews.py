# import psycopg2
# import csv

# try:
#     # Connect to your postgres DB
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     # Open a cursor to perform database operations
#     cur = conn.cursor()

#     print("Connected to the database.")

#     # Execute a command: this creates a new table for shipments_deliveries
#     cur.execute("""
#         CREATE TABLE adesalu8398_staging.shipments_deliveries (
#             shipment_id INT NOT NULL,
#             order_id INT NOT NULL,
#             shipment_date DATE,
#             delivery_date DATE
#         )
#     """)

#     print("Created table adesalu8398_staging.shipments_deliveries.")

#     # Path to the CSV file
#     csv_path = 'shipment_deliveries.csv'

#     # Open the CSV file and load it into the table
#     with open(csv_path, 'r') as f:
#         reader = csv.reader(f)
#         next(reader)  # Skip the header row
#         for row in reader:
#             cur.execute(
#                 "INSERT INTO adesalu8398_staging.shipments_deliveries VALUES (%s, %s, %s, %s)",
#                 row
#             )

#     print("Inserted data into adesalu8398_staging.shipments_deliveries.")

#     # Execute a command: this creates a new table for reviews
#     cur.execute("""
#         CREATE TABLE adesalu8398_staging.reviews (
#             review INT NOT NULL,
#             product_id INT NOT NULL
#         )
#     """)

#     print("Created table adesalu8398_staging.reviews.")

#     # Path to the CSV file
#     csv_path = 'reviews.csv'

#     # Open the CSV file and load it into the table
#     with open(csv_path, 'r') as f:
#         reader = csv.reader(f)
#         next(reader)  # Skip the header row
#         for row in reader:
#             cur.execute(
#                 "INSERT INTO adesalu8398_staging.reviews VALUES (%s, %s)",
#                 row
#             )

#     print("Inserted data into adesalu8398_staging.reviews.")

#     # Commit the changes
#     conn.commit()

# except Exception as e:
#     print(f"An error occurred: {e}")
#     conn.rollback()

# finally:
#     # Close the cursor and the connection
#     if cur is not None:
#         cur.close()
#     if conn is not None:
#         conn.close()
#         print("Closed the connection to the database.")




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

    # Execute a command: this creates a new table for shipments_deliveries
    cur.execute("""
        CREATE TABLE adesalu8398_staging.shipments_deliveries (
            shipment_id INT NOT NULL,
            order_id INT NOT NULL,
            shipment_date DATE,
            delivery_date DATE
        )
    """)

    print("Created table adesalu8398_staging.shipments_deliveries.")

    # Path to the CSV file
    csv_path = 'shipment_deliveries.csv'

    # Open the CSV file and load it into the table
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            # Replace empty strings with None
            row = [value if value != '' else None for value in row]
            cur.execute(
                "INSERT INTO adesalu8398_staging.shipments_deliveries VALUES (%s, %s, %s, %s)",
                row
            )

    print("Inserted data into adesalu8398_staging.shipments_deliveries.")

    # Execute a command: this creates a new table for reviews
    cur.execute("""
        CREATE TABLE adesalu8398_staging.reviews (
            review INT NOT NULL,
            product_id INT NOT NULL
        )
    """)

    print("Created table adesalu8398_staging.reviews.")

    # Path to the CSV file
    csv_path = 'reviews.csv'

    # Open the CSV file and load it into the table
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute(
                "INSERT INTO adesalu8398_staging.reviews VALUES (%s, %s)",
                row
            )

    print("Inserted data into adesalu8398_staging.reviews.")

    # Commit the changes
    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    # Close the cursor and the connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Closed the connection to the database.")

