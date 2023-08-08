# import psycopg2

# def print_table_columns(table_name):
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     cur = conn.cursor()

#     cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")

#     results = cur.fetchall()

#     for result in results:
#         print(result[0])

#     conn.close()

# if __name__ == "__main__":
#     print_table_columns("reviews")


# INSERT INTO adesalu8398_analytics.best_performing_product (
#     ingestion_date,
#     product_name,
#     most_ordered_day,
#     is_public_holiday,
#     tt_review_points,
#     pct_one_star_review,
#     pct_two_star_review,
#     pct_three_star_review,
#     pct_four_star_review,
#     pct_five_star_review,
#     pct_early_shipments,
#     pct_late_shipments
# )
# SELECT
#     CURRENT_DATE,
#     p.product_name,
#     mod.most_ordered_day,
#     CASE
#         WHEN d.day_of_the_week_num BETWEEN 1 AND 5 AND d.working_day = false THEN true
#         ELSE false
#     END AS is_public_holiday,
#     SUM(r.review) AS tt_review_points,
#     SUM(CASE WHEN r.review = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_one_star_review,
#     SUM(CASE WHEN r.review = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_two_star_review,
#     SUM(CASE WHEN r.review = 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_three_star_review,
#     SUM(CASE WHEN r.review = 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_four_star_review,
#     SUM(CASE WHEN r.review = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_five_star_review,
#     SUM(CASE WHEN s.delivery_date < s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_early_shipments,
#     SUM(CASE WHEN s.delivery_date > s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_late_shipments
# FROM
#     adesalu8398_staging.dim_products AS p
#     JOIN
#     adesalu8398_staging.product_most_ordered_day AS mod ON p.product_id = mod.product_id
#     JOIN
#     adesalu8398_staging.dim_dates AS d ON mod.most_ordered_day = d.calendar_dt
#     JOIN
#     adesalu8398_staging.reviews AS r ON p.product_id = r.product_id
#     JOIN
#     adesalu8398_staging.shipments_deliveries AS s ON p.product_id = s.product_id
# WHERE
#     p.product_id = (
#         SELECT
#             product_id
#         FROM
#             adesalu8398_staging.reviews
#         ORDER BY
#             review DESC
#         LIMIT 1
#     )
# GROUP BY
#     p.product_name,
#     mod.most_ordered_day,
#     d.day_of_the_week_num,
#     d.working_day,
#     s.shipment_date,
#     s.delivery_date

import psycopg2

# def fetch_table_column_details(table_name):
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     cur = conn.cursor()

#     cur.execute(f"""
#         SELECT column_name, data_type, is_nullable, column_default
#         FROM information_schema.columns
#         WHERE table_name = '{table_name}';
#     """)

#     results = cur.fetchall()

#     for result in results:
#         print(f"Column Name: {result[0]}, Data Type: {result[1]}, Nullable: {result[2]}, Default: {result[3]}")

#     conn.close()

# if __name__ == "__main__":
#     fetch_table_column_details("reviews")

# def check_duplicate_columns(table_name, column1, column2):
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     cur = conn.cursor()

#     cur.execute(f"SELECT {column1}, {column2} FROM {table_name} WHERE {column1} != {column2};")

#     results = cur.fetchall()

#     if results:
#         print(f"Found {len(results)} rows where {column1} and {column2} are different.")
#     else:
#         print(f"{column1} and {column2} are identical in all rows.")

#     conn.close()

# if __name__ == "__main__":
#     check_duplicate_columns("reviews", "product_id", "product_id")
#     check_duplicate_columns("reviews", "review", "review")


import psycopg2

# def remove_duplicate_columns():
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     cur = conn.cursor()

#     try:
#         # Create a new table without the duplicate columns
#         cur.execute("""
#             CREATE TABLE reviews_temp AS
#             SELECT DISTINCT product_id, review
#             FROM reviews;
#         """)

#         # Drop the old table
#         cur.execute("DROP TABLE reviews;")

#         # Rename the new table to the original name
#         cur.execute("ALTER TABLE reviews_temp RENAME TO reviews;")

#         print("Duplicate columns removed successfully.")
        
#         conn.commit()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     remove_duplicate_columns()

# import psycopg2

# def remove_duplicate_columns():
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     cur = conn.cursor()

#     try:
#         # Rename the old table
#         cur.execute("ALTER TABLE reviews RENAME TO reviews_old;")

#         # Create a new table without the duplicate columns
#         cur.execute("""
#             CREATE TABLE reviews AS
#             SELECT DISTINCT product_id, review
#             FROM reviews_old;
#         """)

#         # Optionally, drop the old table if you don't need it anymore
#         cur.execute("DROP TABLE reviews_old;")

#         print("Duplicate columns removed successfully.")
        
#         conn.commit()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     remove_duplicate_columns()


import psycopg2

# # Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     dbname="d2b_accessment",
#     user="adesalu8398",
#     password="c7CPYwmPGm",
#     host="34.89.230.185",
#     port="5432"
# )
# cur = conn.cursor()

# # SQL to find the product with the highest reviews
# sql_product_reviews = """
#     SELECT product_id, SUM(review) as total_reviews
#     FROM reviews
#     GROUP BY product_id
#     ORDER BY total_reviews DESC
#     LIMIT 1;
# """
# cur.execute(sql_product_reviews)
# highest_reviewed_product, total_review_points = cur.fetchone()

# # SQL to find the day it was ordered the most
# sql_most_ordered_day = f"""
#     SELECT order_date, COUNT(order_date) as order_count
#     FROM orders
#     WHERE product_id = {highest_reviewed_product}
#     GROUP BY order_date
#     ORDER BY order_count DESC
#     LIMIT 1;
# """
# cur.execute(sql_most_ordered_day)
# most_ordered_day, _ = cur.fetchone()

# # SQL to check if that day was a public holiday
# sql_is_public_holiday = f"""
#     SELECT COUNT(*)
#     FROM dim_dates
#     WHERE calendar_dt = '{most_ordered_day}' AND day_of_the_week BETWEEN 1 AND 5 AND working_day = false;
# """
# cur.execute(sql_is_public_holiday)
# is_public_holiday = cur.fetchone()[0] > 0

# # SQL to get percentage distribution of early shipments to late shipments for that product
# sql_shipment_distribution = f"""
#     SELECT 
#         SUM(CASE WHEN delivery_date < shipment_date THEN 1 ELSE 0 END) as early_shipments,
#         SUM(CASE WHEN delivery_date > shipment_date THEN 1 ELSE 0 END) as late_shipments
#     FROM shipment_deliveries
#     WHERE order_id IN (SELECT order_id FROM orders WHERE product_id = {highest_reviewed_product});
# """
# cur.execute(sql_shipment_distribution)
# early_shipments, late_shipments = cur.fetchone()
# total_shipments = early_shipments + late_shipments
# early_shipment_percentage = (early_shipments / total_shipments) * 100
# late_shipment_percentage = (late_shipments / total_shipments) * 100

# print(f"Product with the highest reviews: {highest_reviewed_product}")
# print(f"Most ordered day: {most_ordered_day}")
# print(f"Is public holiday: {is_public_holiday}")
# print(f"Total review points: {total_review_points}")
# print(f"Early shipment percentage: {early_shipment_percentage}%")
# print(f"Late shipment percentage: {late_shipment_percentage}%")

# # Close the connection
# cur.close()
# conn.close()



import psycopg2

# def list_tables_in_public_schema():
#     # Connect to the PostgreSQL database
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )
    
#     # Create a cursor object
#     cur = conn.cursor()
    
#     # Execute the SQL query to fetch table names in the 'public' schema
#     cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    
#     # Fetch all the results
#     tables = cur.fetchall()
    
#     # Close the cursor and the connection
#     cur.close()
#     conn.close()
    
#     # Print the tables
#     for table in tables:
#         print(table[0])

# if __name__ == "__main__":
#     list_tables_in_public_schema()


import psycopg2

def fetch_best_performing_product_metrics():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="d2b_accessment",
        user="adesalu8398",
        password="c7CPYwmPGm",
        host="34.89.230.185",
        port="5432"
    )
    
    # Create a cursor object
    cur = conn.cursor()
    
    # SQL to fetch the product with the highest reviews
    sql_best_product = """
        SELECT product_id, SUM(review) as total_reviews
        FROM reviews
        GROUP BY product_id
        ORDER BY total_reviews DESC
        LIMIT 1;
    """
    
    cur.execute(sql_best_product)
    best_product = cur.fetchone()
    
    product_id = best_product[0]
    total_reviews = best_product[1]
    
    # SQL to fetch the day the product was ordered the most
    sql_most_ordered_day = """
        SELECT order_date, COUNT(order_date) as order_count
        FROM orders
        WHERE product_id = %s
        GROUP BY order_date
        ORDER BY order_count DESC
        LIMIT 1;
    """
    
    cur.execute(sql_most_ordered_day, (product_id,))
    most_ordered_day_data = cur.fetchone()
    
    most_ordered_day = most_ordered_day_data[0]
    
    # Check if the most ordered day is a public holiday
    sql_is_public_holiday = """
        SELECT (day_of_the_week_num BETWEEN 1 AND 5 AND working_day = false) as is_public_holiday
        FROM dim_dates
        WHERE calendar_dt = %s;
    """
    
    cur.execute(sql_is_public_holiday, (most_ordered_day,))
    is_public_holiday = cur.fetchone()[0]
    
    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    # Print the results
    print(f"Product ID with the highest reviews: {product_id}")
    print(f"Total reviews for the product: {total_reviews}")
    print(f"Day the product was ordered the most: {most_ordered_day}")
    print(f"Is the most ordered day a public holiday? {'Yes' if is_public_holiday else 'No'}")

if __name__ == "__main__":
    fetch_best_performing_product_metrics()
