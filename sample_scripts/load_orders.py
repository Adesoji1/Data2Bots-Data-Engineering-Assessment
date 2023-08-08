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

    # Check if the table already exists
    cur.execute("""
        SELECT to_regclass('adesalu8398_staging.orders');
    """)
    result = cur.fetchone()
    if result[0]:
        print("Table adesalu8398_staging.orders already exists.")
    else:
        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE adesalu8398_staging.orders (
                order_id INT NOT NULL,
                customer_id INT NOT NULL,
                order_date DATE NOT NULL,
                product_id VARCHAR NOT NULL,
                unit_price INT NOT NULL,
                quantity INT NOT NULL,
                amount INT NOT NULL
            )
        """)
        print("Created table adesalu8398_staging.orders.")

    # Path to the CSV file
    csv_path = 'orders.csv'

    # Open the CSV file and load it into the table
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute(
                "INSERT INTO adesalu8398_staging.orders VALUES (%s, %s, %s, %s, %s, %s, %s)",
                row
            )

    print("Inserted data into adesalu8398_staging.orders.")

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
