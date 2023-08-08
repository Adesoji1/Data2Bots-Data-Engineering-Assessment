import psycopg2

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

# Execute the query
cur.execute("""
    SELECT product_id, COUNT(*) AS review_count
    FROM adesalu8398_staging.reviews
    GROUP BY product_id
    ORDER BY review_count DESC
    LIMIT 1;
""")
            

# Fetch the results
results = cur.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()
