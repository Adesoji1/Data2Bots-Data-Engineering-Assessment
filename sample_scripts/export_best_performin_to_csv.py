import psycopg2
import csv

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

# Execute the command: this fetches all rows from the best_performing_product table
cur.execute("""
    SELECT *
    FROM adesalu8398_analytics.best_performing_product
""")

# Fetch all rows from the cursor
rows = cur.fetchall()

# Get the column names from the cursor description
column_names = [desc[0] for desc in cur.description]

# Write the rows and column names to a CSV file
with open('best_performing_product.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(column_names)  # write the header
    writer.writerows(rows)  # write the data

# Close the cursor and the connection
cur.close()
conn.close()
