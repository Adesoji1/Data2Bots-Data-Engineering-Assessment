'''
Certainly! To achieve this, we'll follow these steps:

1. Load the CSV files into pandas dataframes.
2. Aggregate and analyze the data to get the desired results.

Here's the Python code using the `pandas` library:

'''
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

    # SQL to get the product with the highest reviews
    sql_highest_reviews = """
        SELECT product_id, COUNT(review) as total_reviews
        FROM reviews
        GROUP BY product_id
        ORDER BY total_reviews DESC
        LIMIT 1;
    """
    cur.execute(sql_highest_reviews)
    product_id, total_reviews = cur.fetchone()

    # SQL to get the day the product was ordered the most
    sql_most_ordered_day = """
        SELECT order_date, COUNT(order_id) as total_orders
        FROM orders
        WHERE product_id = %s
        GROUP BY order_date
        ORDER BY total_orders DESC
        LIMIT 1;
    """
    cur.execute(sql_most_ordered_day, (product_id,))
    most_ordered_day, _ = cur.fetchone()

    # SQL to check if the most ordered day was a public holiday
    sql_is_public_holiday = """
        SELECT COUNT(*) 
        FROM if_common.dim_dates
        WHERE calendar_dt = %s AND day_of_the_week_num BETWEEN 1 AND 5 AND working_day = false;
    """
    cur.execute(sql_is_public_holiday, (most_ordered_day,))
    is_public_holiday = cur.fetchone()[0] > 0

    # SQL to get the total review points for the product
    sql_total_review_points = """
        SELECT SUM(review)
        FROM reviews
        WHERE product_id = %s;
    """
    cur.execute(sql_total_review_points, (product_id,))
    total_review_points = cur.fetchone()[0]

    # SQL to get the percentage distribution of the review points
    sql_pct_review_points = """
        SELECT review, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
        FROM reviews
        WHERE product_id = %s
        GROUP BY review;
    """
    cur.execute(sql_pct_review_points, (product_id,))
    review_distribution = cur.fetchall()

    # SQL to get the percentage distribution of early shipments to late shipments
    sql_shipment_distribution = """
        SELECT
            CASE 
                WHEN delivery_date < shipment_date THEN 'Early'
                ELSE 'Late'
            END as shipment_status,
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
        FROM shipment_deliveries
        JOIN orders ON shipment_deliveries.order_id = orders.order_id
        WHERE orders.product_id = %s
        GROUP BY shipment_status;
    """
    cur.execute(sql_shipment_distribution, (product_id,))
    shipment_distribution = cur.fetchall()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    # Print the results
    print(f"Product ID: {product_id}")
    print(f"Total Reviews: {total_reviews}")
    print(f"Most Ordered Day: {most_ordered_day}")
    print(f"Was it a public holiday? {'Yes' if is_public_holiday else 'No'}")
    print(f"Total Review Points: {total_review_points}")
    print("Review Points Distribution:")
    for review, pct in review_distribution:
        print(f"Review {review}: {pct:.2f}%")
    print("Shipment Distribution:")
    for status, pct in shipment_distribution:
        print(f"{status} Shipments: {pct:.2f}%")

# Call the function
fetch_best_performing_product_metrics()
