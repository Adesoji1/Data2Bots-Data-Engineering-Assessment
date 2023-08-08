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

# Execute the SQL query
cur.execute("""
    SELECT 
        DATE_PART('year', o.order_date) AS year,
        DATE_PART('month', o.order_date) AS month,
        COUNT(*) AS total_orders
    FROM 
        adesalu8398_staging.orders AS o
    JOIN 
        if_common.dim_dates AS d
    ON 
        o.order_date = d.calendar_dt
    WHERE 
        d.day_of_the_week_num BETWEEN 1 AND 5
        AND d.working_day = false
        AND o.order_date >= (CURRENT_DATE - INTERVAL '1 year')
    GROUP BY 
        year, month
    ORDER BY 
        year, month;
""")

# Fetch all the rows
rows = cur.fetchall()

for row in rows:
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()
